import json
import logging

from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic
from ipware.ip import get_client_ip

from conf import tasks
from . import forms
from . import models
from . import viewmixins


class GolfClubListView(viewmixins.PageableMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'booking/golf-club-list.html'

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(status=models.Club.STATUS_CHOICES.open)

        return queryset.order_by('position')


class GolfAreaListView(viewmixins.PageableMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'booking/golf-area-list.html'

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(district__province__area__slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(GolfAreaListView, self).get_context_data(**kwargs)

        cache_key = 'booking.GolfAreaListView.get_context_data({})'.format(self.kwargs['slug'])
        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        context['area'] = cache.get(cache_key)

        if not context['area']:
            context['area'] = models.Area.objects.get(slug=self.kwargs['slug'])

            cache.set(cache_key, context['area'], cache_time)

        return context


class GolfProvinceListView(viewmixins.PageableMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'booking/golf-province-list.html'

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(district__province__slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(GolfProvinceListView, self).get_context_data(**kwargs)

        cache_key = 'booking.GolfProvinceListView.get_context_data({})'.format(self.kwargs['slug'])
        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        context['province'] = cache.get(cache_key)

        if not context['province']:
            context['province'] = models.Province.objects.select_related('area').get(slug=self.kwargs['slug'])

            cache.set(cache_key, context['province'], cache_time)

        return context


class GolfClubBookingCreateView(generic.CreateView):
    logger = logging.getLogger(__name__)

    form_class = forms.GolfClubBookingForm

    template_name = 'booking/golf-club-booking-form.html'

    def __init__(self):
        super(GolfClubBookingCreateView, self).__init__()

        self.club = None
        self.rates = None
        self.holidays = None

    def get_form_kwargs(self):
        kwargs = super(GolfClubBookingCreateView, self).get_form_kwargs()

        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        cache_key = 'booking.GolfClubBookingCreateView.get_form_kwargs(club,{})'.format(self.kwargs['slug'])

        self.club = cache.get(cache_key)

        if not self.club:
            self.club = models.Club.objects \
                .select_related('district', 'district__province', 'district__province__area') \
                .get(slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

            cache.set(cache_key, self.club, cache_time)

        cache_key = 'booking.GolfClubBookingCreateView.get_form_kwargs(rates,{})'.format(self.kwargs['slug'])

        self.rates = cache.get(cache_key)

        if not self.rates:
            self.rates = models.Rate.objects \
                .filter(club__slug=self.kwargs['slug'],
                        season_end__gt=timezone.make_aware(timezone.localtime().today())) \
                .order_by('season_start', 'day_of_week', 'slot_start')

            cache.set(cache_key, self.rates, cache_time)

        cache_key = 'booking.GolfClubBookingCreateView.get_form_kwargs(holidays)'

        self.holidays = cache.get(cache_key)

        if not self.holidays:
            self.holidays = models.Holiday.objects \
                .filter(holiday__gte=timezone.make_aware(timezone.localtime().today()))

            cache.set(cache_key, self.holidays, cache_time)

        kwargs['request'] = self.request
        kwargs['club'] = self.club
        kwargs['rates'] = self.rates
        kwargs['holidays'] = self.holidays

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GolfClubBookingCreateView, self).get_context_data(**kwargs)

        context['club'] = self.club
        context['rates'] = self.rates
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        # Build JSON data
        data = {
            'club': {
                'cart_required': self.club.cart_required,
                'weekdays_min_in_advance': self.club.weekdays_min_in_advance,
                'weekdays_max_in_advance': self.club.weekdays_max_in_advance,
                'weekend_min_in_advance': self.club.weekend_min_in_advance,
                'weekend_max_in_advance': self.club.weekend_max_in_advance,
            },
            'rates': [],
            'holidays': [],
        }

        for rate in self.rates:
            data['rates'].append({
                'season_start': rate.season_start.strftime('%Y-%m-%d'),
                'season_end': rate.season_end.strftime('%Y-%m-%d'),
                'weekday': rate.day_of_week,
                'slot_start': rate.slot_start.strftime('%H:%M'),
                'slot_end': rate.slot_end.strftime('%H:%M'),
                'green_fee': int(rate.green_fee_selling_price),
            })

        for holiday in self.holidays:
            data['holidays'].append(holiday.holiday.strftime('%Y-%m-%d'))

        context['json'] = json.dumps(data)

        return context

    def form_valid(self, form):
        # 1. Setup booking meta information
        form.instance.first_name = self.request.user.first_name
        form.instance.last_name = self.request.user.last_name

        form.instance.total_selling_price = form.cleaned_data['total_selling_price']
        form.instance.total_cost_price = form.cleaned_data['total_cost_price']
        form.instance.status = models.Order.STATUS_CHOICES.booking_opened

        form.instance.ip_address = get_client_ip(self.request)
        form.instance.user = self.request.user
        form.instance.accept_language = self.request.META['HTTP_ACCEPT_LANGUAGE'] \
            if 'HTTP_ACCEPT_LANGUAGE' in self.request.META.keys() else _('No language set')
        form.instance.user_agent = self.request.META['HTTP_USER_AGENT']

        response = super().form_valid(form)

        # 2. Associate booking information (Many to many relationship)
        models.ClubOrderListMembership.objects.create(
            club=form.cleaned_data['club'],
            order=self.object,
            round_date=form.cleaned_data['round_date'],
            round_time=form.cleaned_data['round_time'],
            pax=form.cleaned_data['pax'],
            green_fee_selling_price=form.cleaned_data['green_fee_selling_price'],
            green_fee_cost_price=form.cleaned_data['green_fee_cost_price'],
        )

        # 3. Associate booking change log
        models.ClubOrderChangeLog.objects.create(
            order=self.object,
            user=self.request.user,
            status=models.Order.STATUS_CHOICES.booking_opened,
            total_selling_price=form.cleaned_data['total_selling_price'],
            total_cost_price=form.cleaned_data['total_cost_price'],
            club=form.cleaned_data['club'],
            round_date=form.cleaned_data['round_date'],
            round_time=form.cleaned_data['round_time'],
            pax=form.cleaned_data['pax'],
            green_fee_selling_price=form.cleaned_data['green_fee_selling_price'],
            green_fee_cost_price=form.cleaned_data['green_fee_cost_price'],
        )

        # 4. Notify manager, club authorities, user
        html_message = render_to_string('booking/email/booking_opened_message.txt', {'order': self.object, })
        tasks.send_notification_email.delay(
            _('[WITH THAI] Booking Opened {}-*').format(str(self.object.order_no)[:8]),
            'dummy',
            settings.EMAIL_NO_REPLY,
            self.request.user.email,
            html_message,
        )

        return response

    def get_success_url(self):
        return reverse('booking:order-detail', args=(self.object.order_no,))


class OrderListView(LoginRequiredMixin, generic.ListView):
    context_object_name = 'orders'
    template_name = 'booking/order-list.html'

    def get_queryset(self):
        return models.Order.objects \
            .filter(user=self.request.user) \
            .select_related('user') \
            .prefetch_related('cluborderlistmembership_set__club') \
            .order_by('-created')


class OrderDetailView(LoginRequiredMixin, generic.DetailView):
    context_object_name = 'order'
    template_name = 'booking/order-detail.html'

    def get_object(self, queryset=None):
        # NOTE: This method is overridden because DetailView must be called with either an object pk or a slug.
        queryset = models.Order.objects \
            .select_related('user') \
            .prefetch_related('cluborderlistmembership_set__club',
                              'cluborderchangelog_set__user') \
            .filter(order_no=self.kwargs['uuid'])

        return get_object_or_404(queryset)


class GolfClubBookingJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
            'club': {},
            'rates': [],
            'holidays': [],
        }

        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        cache_key = 'booking.GolfClubBookingJson.render_to_response(club,{})'.format(self.kwargs['slug'])

        club = cache.get(cache_key)

        if not club:
            club = models.Club.objects \
                .select_related('district', 'district__province', 'district__province__area') \
                .get(slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

            cache.set(cache_key, club, cache_time)

        data['club']['cart_required'] = club.cart_required
        data['club']['weekdays_min_in_advance'] = club.weekdays_min_in_advance
        data['club']['weekdays_max_in_advance'] = club.weekdays_max_in_advance
        data['club']['weekend_min_in_advance'] = club.weekend_min_in_advance
        data['club']['weekend_max_in_advance'] = club.weekend_max_in_advance

        cache_key = 'booking.GolfClubBookingJson.render_to_response(rates,{})'.format(self.kwargs['slug'])

        rates = cache.get(cache_key)

        if not rates:
            rates = models.Rate.objects \
                .filter(club__slug=self.kwargs['slug'],
                        season_end__gt=timezone.make_aware(timezone.localtime().today())) \
                .order_by('season_start', 'day_of_week', 'slot_start')

            cache.set(cache_key, rates, cache_time)

        for rate in rates:
            data['rates'].append({
                'season_start': rate.season_start,
                'season_end': rate.season_end,
                'weekday': rate.day_of_week,
                'slot_start': rate.slot_start.strftime('%H:%M'),
                'slot_end': rate.slot_end.strftime('%H:%M'),
                'green_fee': int(rate.green_fee_selling_price),
            })

        cache_key = 'booking.GolfClubBookingJson.render_to_response(holidays)'

        holidays = cache.get(cache_key)

        if not holidays:
            holidays = models.Holiday.objects \
                .filter(holiday__gte=timezone.make_aware(timezone.localtime().today()))

            cache.set(cache_key, holidays, cache_time)

        for holiday in holidays:
            data['holidays'].append(holiday.holiday)

        return JsonResponse(
            data,
            json_dumps_params={'ensure_ascii': False},
            **response_kwargs
        )

    def get_queryset(self):
        return models.Rate.objects \
            .filter(club__slug=self.kwargs['slug'], season_end__gt=timezone.make_aware(timezone.localtime().today())) \
            .order_by('season_start', 'day_of_week', 'slot_start')

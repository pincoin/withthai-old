import logging

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.urls import reverse
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.views import generic
from ipware.ip import get_ip

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

        cache_key = 'golf.GolfAreaListView.get_context_data({})'.format(self.kwargs['slug'])
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

        cache_key = 'golf.GolfProvinceListView.get_context_data({})'.format(self.kwargs['slug'])
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

    def get_form_kwargs(self):
        print('get_form_kwargs')
        kwargs = super(GolfClubBookingCreateView, self).get_form_kwargs()

        self.club = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .get(slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

        self.rates = models.Rate.objects \
            .filter(club__slug=self.kwargs['slug'], season_end__gt=timezone.make_aware(timezone.localtime().today())) \
            .order_by('season_start', 'day_of_week', 'slot_start')

        kwargs['request'] = self.request
        kwargs['club'] = self.club
        kwargs['rates'] = self.rates

        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GolfClubBookingCreateView, self).get_context_data(**kwargs)

        context['club'] = self.club
        context['rates'] = self.rates
        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY

        return context

    def form_valid(self, form):
        # 1. Construct booking list

        # 2. Setup booking meta information
        form.instance.total_selling_price = 0
        form.instance.total_cost_price = 0

        form.instance.ip_address = get_ip(self.request)
        form.instance.user = self.request.user
        form.instance.accept_language = self.request.META['HTTP_ACCEPT_LANGUAGE'] \
            if 'HTTP_ACCEPT_LANGUAGE' in self.request.META.keys() else _('No language set')
        form.instance.user_agent = self.request.META['HTTP_USER_AGENT']

        response = super().form_valid(form)

        # 3. Associate booking to order

        # 4. Notify manager, club authorities, user

        return response

    def get_success_url(self):
        return reverse('booking:golf-club-list', args=())


class GolfClubBookingJson(generic.TemplateView):
    def render_to_response(self, context, **response_kwargs):
        data = {
            'club': {},
            'rates': [],
            'holidays': [],
        }

        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        cache_key = 'golf.GolfClubBookingJson.render_to_response(club,{})'.format(self.kwargs['slug'])

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

        cache_key = 'golf.GolfClubBookingJson.render_to_response(rates,{})'.format(self.kwargs['slug'])

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

        cache_key = 'golf.GolfClubBookingJson.render_to_response(holidays)'

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

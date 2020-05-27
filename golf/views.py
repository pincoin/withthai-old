import logging

from django.conf import settings
from django.core.cache import cache
from django.urls import reverse
from django.utils import timezone
from django.views import generic

from . import forms
from . import models
from . import viewmixins


class GolfClubListView(viewmixins.PageableMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'golf/golf-club-list.html'

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(status=models.Club.STATUS_CHOICES.open)

        return queryset.order_by('position')


class GolfAreaListView(viewmixins.PageableMixin, generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'golf/golf-area-list.html'

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

    template_name = 'golf/golf-province-list.html'

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


class GolfClubBookingForm(generic.edit.FormMixin, generic.DetailView):
    logger = logging.getLogger(__name__)
    context_object_name = 'club'

    form_class = forms.GolfClubBookingForm

    template_name = 'golf/golf-club-booking-form.html'

    def get_queryset(self):
        return models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(slug=self.kwargs['slug'], status=models.Club.STATUS_CHOICES.open)

    def get_form_kwargs(self):
        kwargs = super(GolfClubBookingForm, self).get_form_kwargs()
        return kwargs

    def get_context_data(self, **kwargs):
        context = super(GolfClubBookingForm, self).get_context_data(**kwargs)

        context['google_maps_api_key'] = settings.GOOGLE_MAPS_API_KEY
        context['rates'] = models.Rate.objects \
            .filter(club__slug=self.kwargs['slug'], season_end__gt=timezone.make_aware(timezone.localtime().today())) \
            .order_by('season_start', 'day_of_week', 'slot_start')

        return context

    def form_valid(self, form):
        print(form.data)
        return super().form_valid(form)

    def form_invalid(self, form):
        print(form.errors)
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('golf:golf-club-list', args=())

import logging

from django.conf import settings
from django.core.cache import cache
from django.views import generic

from . import models


class GolfClubListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'golf/golf-club-list.html'

    block_size = 5

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area')

        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(GolfClubListView, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / GolfClubListView.block_size) * GolfClubListView.block_size
        end_index = min(start_index + GolfClubListView.block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]
        return context

    def get_paginate_by(self, queryset):
        return 10


class GolfAreaListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'golf/golf-area-list.html'

    block_size = 5

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(district__province__area__slug=self.kwargs['slug'])

        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(GolfAreaListView, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / GolfClubListView.block_size) * GolfClubListView.block_size
        end_index = min(start_index + GolfClubListView.block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        cache_key = 'golf.GolfAreaListView.get_context_data({})'.format(self.kwargs['slug'])
        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        context['area'] = cache.get(cache_key)

        if not context['area']:
            context['area'] = models.Area.objects.get(slug=self.kwargs['slug'])

            cache.set(cache_key, context['area'], cache_time)

        return context

    def get_paginate_by(self, queryset):
        return 10


class GolfProvinceListView(generic.ListView):
    logger = logging.getLogger(__name__)
    context_object_name = 'clubs'

    template_name = 'golf/golf-province-list.html'

    block_size = 5

    def get_queryset(self):
        queryset = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(district__province__slug=self.kwargs['slug'])

        return queryset.order_by('position')

    def get_context_data(self, **kwargs):
        context = super(GolfProvinceListView, self).get_context_data(**kwargs)

        start_index = int((context['page_obj'].number - 1) / GolfClubListView.block_size) * GolfClubListView.block_size
        end_index = min(start_index + GolfClubListView.block_size, len(context['paginator'].page_range))

        context['page_range'] = context['paginator'].page_range[start_index:end_index]

        cache_key = 'golf.GolfProvinceListView.get_context_data({})'.format(self.kwargs['slug'])
        cache_time = settings.CACHES['default']['TIMEOUT_DAY']

        context['province'] = cache.get(cache_key)

        if not context['province']:
            context['province'] = models.Province.objects.select_related('area').get(slug=self.kwargs['slug'])

            cache.set(cache_key, context['province'], cache_time)

        return context

    def get_paginate_by(self, queryset):
        return 10

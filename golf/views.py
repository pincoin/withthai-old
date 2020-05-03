import logging

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
        return 20

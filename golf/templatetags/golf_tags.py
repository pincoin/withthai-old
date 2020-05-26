from django import template
from django.conf import settings
from django.core.cache import cache

from .. import models

register = template.Library()


@register.simple_tag
def get_clubs():
    return models.Club.objects.filter(status=models.Club.STATUS_CHOICES.open)


@register.simple_tag
def get_areas():
    cache_key = 'golf.templatetags.golf_tags.get_areas()'
    cache_time = settings.CACHES['default']['TIMEOUT_DAY']

    areas = cache.get(cache_key)

    if not areas:
        areas = models.Area.objects \
            .all() \
            .order_by('position')

        cache.set(cache_key, areas, cache_time)

    return areas


@register.simple_tag
def get_provinces(slug):
    cache_key = 'golf.templatetags.golf_tags.get_areas({})'.format(slug)
    cache_time = settings.CACHES['default']['TIMEOUT_DAY']

    provinces = cache.get(cache_key)

    if not provinces:
        provinces = models.Province.objects \
            .select_related('area') \
            .filter(area__slug=slug) \
            .order_by('position')

        cache.set(cache_key, provinces, cache_time)

    return provinces


@register.simple_tag
def get_golf_club_list(clublist_code):
    cache_key = 'golf.templatetags.shop_tags.get_golf_club_list({})'.format(clublist_code)
    cache_time = settings.CACHES['default']['TIMEOUT_DAY']

    clubs = cache.get(cache_key)

    if not clubs:
        clubs = models.Club.objects \
            .select_related('district', 'district__province', 'district__province__area') \
            .filter(status=models.Club.STATUS_CHOICES.open, clublist__code=clublist_code) \
            .order_by('clublistmembership__position')

        cache.set(cache_key, clubs, cache_time)

    return clubs

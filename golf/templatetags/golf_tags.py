from django import template
from django.conf import settings
from django.core.cache import cache

from .. import models

register = template.Library()


@register.simple_tag
def get_clubs():
    return models.Club.objects.all()


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
            .filter(area__slug=slug) \
            .order_by('position')

        cache.set(cache_key, provinces, cache_time)

    return provinces

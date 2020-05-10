from django import template

from .. import models

register = template.Library()


@register.simple_tag
def get_clubs():
    return models.Club.objects.all()


@register.simple_tag
def get_areas():
    return models.Area.objects.all().order_by('position')


@register.simple_tag
def get_provinces():
    return models.Province.objects.all().order_by('position')

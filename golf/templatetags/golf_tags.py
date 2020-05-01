from django import template

from .. import models

register = template.Library()


@register.simple_tag
def get_recent_posts():
    return models.Club.objects.all()

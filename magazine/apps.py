from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _


class MagazineConfig(AppConfig):
    name = 'magazine'
    verbose_name = _('Magazine')

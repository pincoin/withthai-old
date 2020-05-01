from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils import models as model_utils_models


class Holiday(model_utils_models.TimeStampedModel):
    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
    )

    title = models.CharField(
        verbose_name=_('Holiday name'),
        max_length=255,
    )

    holiday = models.DateField(
        verbose_name=_('Holiday day'),
        db_index=True,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Holiday')
        verbose_name_plural = _('Holidays')

        unique_together = ('holiday', 'country')

    def __str__(self):
        return '{} {} {}'.format(self.title, self.holiday, self.country)


class Area(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
        verbose_name=_('Area english name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('Area Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('Area Korean name'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return '{}'.format(self.title_english)


class Province(model_utils_models.TimeStampedModel):
    title_enlish = models.CharField(
        verbose_name=_('Province English name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('Province Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('Province Korean name'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return '{}'.format(self.title_enlish)


class District(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
        verbose_name=_('District English name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('District Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('District Korean name'),
        max_length=255,
    )

    class Meta:
        verbose_name = _('District')
        verbose_name_plural = _('Districts')

    def __str__(self):
        return '{}'.format(self.title_english)


class Club(model_utils_models.TimeStampedModel):
    HOLE_CHOICES = Choices(
        (0, 'eighteen', _('18 Holes')),
        (1, 'nine', _('9 Holes')),
        (2, 'twentyseven', _('27 Holes')),
        (3, 'thirtysix', _('36 Holes')),
    )

    COUNTRY_CHOICES = Choices(
        (1, 'thailand', _('Thailand')),
        (2, 'south_korea', _('South Korea')),
        (3, 'japan', _('Japan')),
        (4, 'china', _('China')),
    )

    title_english = models.CharField(
        verbose_name=_('Golf club English name'),
        max_length=255,
    )

    title_thai = models.CharField(
        verbose_name=_('Golf club Thai name'),
        max_length=255,
    )

    title_korean = models.CharField(
        verbose_name=_('Golf club Korean name'),
        max_length=255,
    )

    area = models.ForeignKey(
        'golf.Area',
        verbose_name=_('Location area'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    province = models.ForeignKey(
        'golf.Province',
        verbose_name=_('Province'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    district = models.ForeignKey(
        'golf.District',
        verbose_name=_('District'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=16,
        blank=True,
        null=True,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        max_length=255,
        blank=True,
        null=True,
    )

    fax = models.CharField(
        verbose_name=_('Fax number'),
        max_length=16,
        blank=True,
        null=True,
    )

    website = models.URLField(
        verbose_name=_('Website'),
        max_length=255,
        blank=True,
        null=True,
    )

    hole = models.IntegerField(
        verbose_name=_('No. of holes'),
        choices=HOLE_CHOICES,
        default=HOLE_CHOICES.eighteen,
        db_index=True,
    )

    country = models.IntegerField(
        verbose_name=_('Country code'),
        choices=COUNTRY_CHOICES,
        default=COUNTRY_CHOICES.thailand,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title_english, self.email, self.phone)


class Price(model_utils_models.TimeStampedModel):
    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    club = models.ForeignKey(
        'golf.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    season_start = models.DateField(
        verbose_name=_('Season start date'),
    )

    season_end = models.DateField(
        verbose_name=_('Season end date'),
    )

    day_of_week = models.IntegerField(
        verbose_name=_('Day of week'),
        choices=DAY_CHOICES,
        default=DAY_CHOICES.weekday,
        db_index=True,
    )

    slot_start = models.DateField(
        verbose_name=_('Slot start time'),
    )

    slot_end = models.DateField(
        verbose_name=_('Slot end time'),
    )

    green_fee_selling_price = models.DecimalField(
        verbose_name=_('Green fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    green_fee_cost_price = models.DecimalField(
        verbose_name=_('Green fee cost price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    caddie_fee_selling_price = models.DecimalField(
        verbose_name=_('Caddie fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    caddie_fee_cost_price = models.DecimalField(
        verbose_name=_('Caddie fee cost price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    cart_fee_selling_price = models.DecimalField(
        verbose_name=_('Cart fee selling price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    cart_fee_cost_price = models.DecimalField(
        verbose_name=_('Cart fee cost price'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Price')
        verbose_name_plural = _('Prices')

    def __str__(self):
        return '{} {}'.format(self.season_start, self.season_end)

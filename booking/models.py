import uuid

from django.conf import settings
from django.db import models
from django.utils.timezone import now
from django.utils.translation import gettext_lazy as _
from easy_thumbnails.fields import ThumbnailerImageField
from model_utils import Choices
from model_utils import models as model_utils_models


def upload_directory_path(instance, filename):
    # File will be uploaded to MEDIA_ROOT/golf/<today>/<uuid>.<ext>
    return 'golf/{}/{}.{}'.format(now().strftime('%Y-%m-%d'), uuid.uuid4(), filename.split('.')[-1])


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

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Area')
        verbose_name_plural = _('Areas')

    def __str__(self):
        return '{}'.format(self.title_english)


class Province(model_utils_models.TimeStampedModel):
    title_english = models.CharField(
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

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    area = models.ForeignKey(
        'booking.Area',
        verbose_name=_('Location area'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Province')
        verbose_name_plural = _('Provinces')

    def __str__(self):
        return '{}'.format(self.title_english)


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

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    province = models.ForeignKey(
        'booking.Province',
        verbose_name=_('Province'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
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

    STATUS_CHOICES = Choices(
        (0, 'open', _('Club open')),
        (1, 'closed', _('Club closed')),
    )

    title_english = models.CharField(
        verbose_name=_('Golf club English name'),
        max_length=255,
        db_index=True,
    )

    title_thai = models.CharField(
        verbose_name=_('Golf club Thai name'),
        max_length=255,
        db_index=True,
    )

    title_korean = models.CharField(
        verbose_name=_('Golf club Korean name'),
        max_length=255,
        db_index=True,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        db_index=True,
        unique=True,
        allow_unicode=True,
    )

    district = models.ForeignKey(
        'booking.District',
        verbose_name=_('District'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    phone = models.CharField(
        verbose_name=_('Phone number'),
        max_length=32,
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

    address = models.CharField(
        verbose_name=_('Golf club address'),
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

    green_fee_selling_price = models.DecimalField(
        verbose_name=_('Start from'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
        db_index=True,
    )

    caddie_fee_selling_price = models.DecimalField(
        verbose_name=_('Caddie fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
        db_index=True,
    )

    cart_fee_selling_price = models.DecimalField(
        verbose_name=_('Cart fee'),
        max_digits=11,
        decimal_places=2,
        help_text=_('THB'),
        db_index=True,
    )

    max_pax = models.IntegerField(
        verbose_name=_('Max PAX'),
        default=4,
    )

    cart_required = models.IntegerField(
        verbose_name=_('Require golf cart'),
        default=0,
        db_index=True,
    )

    weekdays_min_in_advance = models.IntegerField(
        verbose_name=_('Weekdays minimum in advance'),
        default=1,
        db_index=True,
    )

    weekdays_max_in_advance = models.IntegerField(
        verbose_name=_('Weekdays maximum in advance'),
        default=30,
        db_index=True,
    )

    weekend_min_in_advance = models.IntegerField(
        verbose_name=_('Weekend minimum in advance'),
        default=1,
        db_index=True,
    )

    weekend_max_in_advance = models.IntegerField(
        verbose_name=_('Weekend maximum in advance'),
        default=7,
        db_index=True,
    )

    thumbnail1 = ThumbnailerImageField(
        verbose_name=_('Thumbnail 1'),
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )

    thumbnail2 = ThumbnailerImageField(
        verbose_name=_('Thumbnail 2'),
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )

    thumbnail3 = ThumbnailerImageField(
        verbose_name=_('Thumbnail 3'),
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )

    thumbnail4 = ThumbnailerImageField(
        verbose_name=_('Thumbnail 4'),
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )

    thumbnail5 = ThumbnailerImageField(
        verbose_name=_('Thumbnail 5'),
        upload_to=upload_directory_path,
        blank=True,
        null=True,
    )

    latitude = models.DecimalField(
        verbose_name=_('Latitude'),
        max_digits=9,
        decimal_places=6,
        default=0,
    )

    longitude = models.DecimalField(
        verbose_name=_('Longitude'),
        max_digits=9,
        decimal_places=6,
        default=0,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
        default=0,
        db_index=True,
    )

    status = models.IntegerField(
        verbose_name=_('Club status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.open,
        db_index=True,
    )

    class Meta:
        verbose_name = _('Golf club')
        verbose_name_plural = _('Golf clubs')

    def __str__(self):
        return '{} {} {}'.format(self.title_english, self.email, self.phone)


class Rate(model_utils_models.TimeStampedModel):
    DAY_CHOICES = Choices(
        (0, 'weekday', _('Weekday')),
        (1, 'weekend', _('Weekend')),
    )

    RATE_CHOICES = Choices(
        (0, 'day_golf', _('Day golf')),
        (1, 'day_golf_1', _('Day golf 1st round')),
        (2, 'day_golf_1', _('Day golf 2nd round')),
        (3, 'twilight_golf', _('Twilight golf')),
        (4, 'night_golf', _('Night golf')),
    )

    club = models.ForeignKey(
        'booking.Club',
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

    slot_start = models.TimeField(
        verbose_name=_('Slot start time'),
    )

    slot_end = models.TimeField(
        verbose_name=_('Slot end time'),
    )

    title = models.IntegerField(
        verbose_name=_('Rate title'),
        choices=RATE_CHOICES,
        default=RATE_CHOICES.day_golf,
        db_index=True,
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
        verbose_name = _('Service rate')
        verbose_name_plural = _('Service rates')

    def __str__(self):
        return '{} {}'.format(self.season_start, self.season_end)


class ClubList(model_utils_models.TimeStampedModel):
    title = models.CharField(
        verbose_name=_('Club list title'),
        max_length=255,
    )

    code = models.CharField(
        verbose_name=_('Club list code'),
        max_length=255,
    )

    clubs = models.ManyToManyField(Club, through='ClubListMembership')

    class Meta:
        verbose_name = _('Golf club list')
        verbose_name_plural = _('Golf club lists')

    def __str__(self):
        return self.title


class ClubListMembership(models.Model):
    club = models.ForeignKey(
        'booking.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    club_list = models.ForeignKey(
        'booking.ClubList',
        verbose_name=_('Golf club list'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    position = models.IntegerField(
        verbose_name=_('Position'),
    )

    class Meta:
        verbose_name = _('Golf club list membership')
        verbose_name_plural = _('Golf club list membership')


class Order(model_utils_models.SoftDeletableModel, model_utils_models.TimeStampedModel):
    # TODO: order status != payment status
    # 전액환불요청 (total refund requested)
    # 부분환불요청 (partial refund requested)
    # 전액환불됨 (total refund)
    # 부분환불됨 (partial refund)
    STATUS_CHOICES = Choices(
        (0, 'order_opened', _('Booking opened')),
        (1, 'order_pending', _('Booking pending')),
        (2, 'order_offered', _('Booking offered')),
        (3, 'payment_completed', _('Payment completed')),
        (4, 'order_confirmed', _('Booking confirmed')),
        (5, 'order_unavailable', _('Booking unavailable')),
        (6, 'payment_adjustment', _('Payment adjustment')),
        (7, 'payment_adjusted', _('Payment adjusted')),
        (8, 'refund_requested', _('Refund requested')),
        (9, 'refund_pending', _('Refund pending')),
        (10, 'refunded1', _('Refunded')),  # original order
        (11, 'refunded2', _('Refunded')),  # refund order
        (12, 'voided', _('Voided')),
    )

    order_no = models.UUIDField(
        verbose_name=_('Order no'),
        unique=True,
        default=uuid.uuid4,
        editable=False
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('User'),
        db_index=True,
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    last_name = models.CharField(
        verbose_name=_('Last name'),
        max_length=64,
        blank=True,
    )

    first_name = models.CharField(
        verbose_name=_('First name'),
        max_length=64,
        blank=True,
    )

    user_agent = models.TextField(
        verbose_name=_('User-agent'),
        blank=True,
    )

    accept_language = models.TextField(
        verbose_name=_('Accept-language'),
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    transaction_id = models.CharField(
        verbose_name=_('Transaction ID'),
        max_length=64,
        blank=True,
    )

    status = models.IntegerField(
        verbose_name=_('Order status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.order_opened,
        db_index=True,
    )

    # Max = 999,999,999
    total_selling_price = models.DecimalField(
        verbose_name=_('Total selling price'),
        max_digits=11,
        decimal_places=0,
        default=0,
    )

    total_cost_price = models.DecimalField(
        verbose_name=_('Total cost price'),
        max_digits=11,
        decimal_places=0,
        default=0,
    )

    message = models.TextField(
        verbose_name=_('Order message'),
        blank=True,
    )

    parent = models.ForeignKey(
        'self',
        verbose_name=_('Parent order'),
        db_index=True,
        null=True,
        on_delete=models.CASCADE,
    )

    clubs = models.ManyToManyField(Club, through='ClubOrderListMembership')

    class Meta:
        verbose_name = _('Booking order')
        verbose_name_plural = _('Booking orders')

    def __str__(self):
        return '{} {} {}'.format(self.user, self.total_selling_price, self.created)


class ClubOrderListMembership(models.Model):
    club = models.ForeignKey(
        'booking.Club',
        verbose_name=_('Golf club'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    order = models.ForeignKey(
        'booking.Order',
        verbose_name=_('Order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    round_date = models.DateField(
        verbose_name=_('Round date'),
        db_index=True,
    )

    round_time = models.TimeField(
        verbose_name=_('Round time'),
        db_index=True,
    )

    pax = models.IntegerField(
        verbose_name=_('PAX'),
        default=4,
    )

    green_fee_selling_price = models.DecimalField(
        verbose_name=_('Green fee selling price'),
        max_digits=11,
        decimal_places=0,
        default=0,
        help_text=_('THB'),
    )

    green_fee_cost_price = models.DecimalField(
        verbose_name=_('Green fee cost price'),
        max_digits=11,
        decimal_places=0,
        default=0,
        help_text=_('THB'),
    )

    class Meta:
        verbose_name = _('Golf club order list membership')
        verbose_name_plural = _('Golf club order list membership')


class OrderSales(model_utils_models.TimeStampedModel):
    PAYMENT_METHOD_CHOICES = Choices(
        (0, 'credit_card', _('Credit Card')),
        (1, 'bank_transfer', _('Bank Transfer')),
        (2, 'paypal', _('PayPal')),
    )

    CATEGORY_CHOICES = Choices(
        (0, 'payment', _('Payment')),
        (1, 'refunded', _('Refund')),
        (2, 'purchase', _('Purchase')),
    )

    order = models.ForeignKey(
        'booking.Order',
        verbose_name=_('Order'),
        db_index=True,
        on_delete=models.CASCADE,
    )

    payment_method = models.IntegerField(
        verbose_name=_('Payment method'),
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES.credit_card,
        db_index=True,
    )

    category = models.IntegerField(
        verbose_name=_('Transaction category'),
        choices=PAYMENT_METHOD_CHOICES,
        default=PAYMENT_METHOD_CHOICES.credit_card,
        db_index=True,
    )

    amount = models.DecimalField(
        verbose_name=_('Amount'),
        max_digits=11,
        decimal_places=0,
    )

    transaction_date = models.DateTimeField(
        verbose_name=_('Transaction date'),
    )

    class Meta:
        verbose_name = _('Order sales transaction')
        verbose_name_plural = _('Order sales transactions')

    def __str__(self):
        return 'order - {} / transaction - {} {} {}'.format(
            self.order.order_no, self.payment_method, self.amount, self.transaction_date
        )


class Asset(model_utils_models.TimeStampedModel):
    CODE_CHOICES = Choices(
        (0, 'payment_gateway', _('GB prime pay')),
        (1, 'petty_cash', _('Petty cash')),
        (2, 'passbook_krungsri', _('Passbook Krungsri')),
        (3, 'passbook_kasikorn', _('Passbook Kasikorn')),
    )

    code = models.IntegerField(
        verbose_name=_('Asset code'),
        choices=CODE_CHOICES,
        default=CODE_CHOICES.payment_gateway,
        db_index=True,
    )

    title = models.CharField(
        verbose_name=_('Asset name'),
        max_length=255,
    )

    balance = models.DecimalField(
        verbose_name=_('Asset balance'),
        max_digits=11,
        decimal_places=0,
    )

    class Meta:
        verbose_name = _('Asset')
        verbose_name_plural = _('Assets')

    def __str__(self):
        return 'title - {} / balance - {}'.format(self.title, self.balance)

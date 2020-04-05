import uuid

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from model_utils import Choices
from model_utils.models import TimeStampedModel
from mptt.fields import TreeForeignKey
from mptt.models import MPTTModel


class AbstractPage(TimeStampedModel):
    title = models.CharField(
        verbose_name=_('Title'),
        max_length=255,
        help_text=_("The page title as you'd like it to be seen by the public"),
    )

    description = models.CharField(
        verbose_name=_('Description'),
        max_length=255,
        help_text=_("A short description not longer than 155 characters. Don't use double quotes."),
        blank=True,
    )

    keywords = models.CharField(
        verbose_name=_('Keywords'),
        max_length=255,
        help_text=_("A comma-separated list of keywords. Don't use double quotes."),
        blank=True,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Owner'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    class Meta:
        abstract = True


class AbstractCategory(TimeStampedModel, MPTTModel):
    parent = TreeForeignKey(
        'self',
        verbose_name=_('Parent'),
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    title = models.CharField(
        verbose_name=_('Title'),
        max_length=128,
    )

    slug = models.SlugField(
        verbose_name=_('Slug'),
        help_text=_('A short label containing only letters, numbers, underscores or hyphens for URL'),
        max_length=255,
        unique=True,
        allow_unicode=True,
    )

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['created']


class AbstractAttachment(models.Model):
    name = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('File name'),
    )

    # PK is a private identifier
    uid = models.UUIDField(
        verbose_name=_('Public identifier'),
        unique=True,
        default=uuid.uuid4,
        editable=False,
    )

    file = models.FileField(
        verbose_name=_('Uploaded file'),
        upload_to="attachments",
    )

    created = models.DateTimeField(
        verbose_name=_('Created time'),
        auto_now_add=True,
    )

    class Meta:
        abstract = True
        verbose_name = _('Attachment')
        verbose_name_plural = _('Attachments')

    def __str__(self):
        return self.name


class AbstractComment(TimeStampedModel, MPTTModel):
    STATUS_CHOICES = Choices(
        (0, 'approved', _('Approved')),
        (1, 'flagged', _('Flagged')),
        (2, 'deleted', _('Deleted')),
    )

    content = models.TextField(
        verbose_name=_('Content'),
    )

    parent = TreeForeignKey(
        'self',
        verbose_name=_('Parent'),
        blank=True,
        null=True,
        db_index=True,
        on_delete=models.SET_NULL,
    )

    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        verbose_name=_('Owner'),
        null=True,
        blank=True,
        editable=True,
        on_delete=models.SET_NULL,
    )

    username = models.CharField(
        verbose_name=_('Username'),
        max_length=32,
        null=True,
        blank=True,
    )

    email = models.EmailField(
        verbose_name=_('Email address'),
        null=True,
        blank=True,
    )

    url = models.URLField(
        verbose_name=_('Website URL'),
        null=True,
        blank=True,
    )

    ip_address = models.GenericIPAddressField(
        verbose_name=_('IP address'),
    )

    status = models.IntegerField(
        verbose_name=_('Status'),
        choices=STATUS_CHOICES,
        default=STATUS_CHOICES.approved,
        db_index=True,
    )

    class Meta:
        abstract = True

    class MPTTMeta:
        order_insertion_by = ['-created']

    def __str__(self):
        return '{} comment'.format(self.owner)


class Google(TimeStampedModel):
    site_id = models.IntegerField(
        verbose_name=_('Site ID'),
    )

    analytics_uid = models.CharField(
        verbose_name=_('Google Analytics UA-ID'),
        max_length=128,
        blank=True,
        null=True,
    )

    class Meta:
        verbose_name = _('Google Service')
        verbose_name_plural = _('Google Services')

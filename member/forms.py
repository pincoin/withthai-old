from django import forms
from django.contrib.auth.models import Group
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _

from . import models


class MemberSignupForm(forms.Form):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        help_text=_('First name written in English'),
        widget=forms.TextInput(),
        validators=[RegexValidator('^[A-Z]+$', message=_('Uppercase alphabet only')), ],
    )

    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        help_text=_('Last name written in English'),
        widget=forms.TextInput(),
        validators=[RegexValidator('^[A-Z]+$', message=_('Uppercase alphabet only')), ],
    )

    phone = forms.CharField(
        label=_('Telephone'),
        max_length=20,
        widget=forms.TextInput(),
        help_text=_('Digits or plus sign only'),
        validators=[RegexValidator('^\+?1?\d{9,20}$', message=_('Invalid phone number format')), ],
    )

    def __init__(self, *args, **kwargs):
        super(MemberSignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        # Required fields for Django default model
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()

        # Default group: customers
        g = Group.objects.get(name='customers')
        user.groups.add(g)
        user.save()

        # Required fields for profile model
        profile = models.Profile()
        profile.user = user

        profile.save()

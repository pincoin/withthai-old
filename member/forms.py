from django import forms
from django.utils.translation import ugettext_lazy as _

from . import models


class MemberSignupForm(forms.Form):
    first_name = forms.CharField(
        label=_('First name'),
        max_length=30,
        help_text=_('First name written in English'),
        widget=forms.TextInput(),
    )

    last_name = forms.CharField(
        label=_('Last name'),
        max_length=30,
        help_text=_('Last name written in English'),
        widget=forms.TextInput(),
    )

    phone = forms.RegexField(
        label=_('Telephone'),
        widget=forms.TextInput(),
        regex=r'^\+?1?\d{9,15}$',
        error_messages={
            'invalid': _('Invalid phone number format'),
        }
    )

    def __init__(self, *args, **kwargs):
        super(MemberSignupForm, self).__init__(*args, **kwargs)

    def signup(self, request, user):
        # Required fields for Django default model
        user.first_name = self.cleaned_data['first_name'].strip()
        user.last_name = self.cleaned_data['last_name'].strip()

        # Required fields for profile model
        profile = models.Profile()
        profile.user = user

        user.save()
        profile.save()

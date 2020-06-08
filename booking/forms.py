from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class GolfClubBookingForm(forms.ModelForm):
    PAX_CHOICES = (
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
        ('4', '4'),
        ('5', '5'),
        ('6', '6'),
    )

    round_date = forms.DateField(required=True)

    round_time = forms.TimeField(required=True)

    pax = forms.ChoiceField(choices=PAX_CHOICES, required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.club = kwargs.pop('club', None)
        self.rates = kwargs.pop('rates', None)

        super(GolfClubBookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Order
        fields = []

    def clean_round_date(self):
        data = self.cleaned_data['round_date']

        # raise forms.ValidationError(_('Invalid round date'))

        return data

    def clean_round_time(self):
        data = self.cleaned_data['round_time']

        # raise forms.ValidationError(_('Invalid round time'))

        return data

    def clean_pax(self):
        data = self.cleaned_data['pax']

        # raise forms.ValidationError(_('Invalid PAX'))

        return data

    def clean(self):
        super().clean()

        if not self.request.user.is_authenticated or 'customers' not in self.request.user.groups.all():
            raise forms.ValidationError(_('You have to sign in as a customer for booking.'))


class SearchForm(forms.Form):
    q = forms.CharField(
        label=_('Search word'),
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
                'placeholder': _('search word'),
                'required': 'True',
            }
        ),
    )

    def __init__(self, *args, **kwargs):
        q = kwargs.pop('q', '')

        super(SearchForm, self).__init__(*args, **kwargs)

        self.fields['q'].initial = q

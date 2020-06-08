from django import forms
from django.utils.translation import gettext_lazy as _

from . import models


class GolfClubBookingForm(forms.ModelForm):
    round_date = forms.DateField(required=True)

    round_time = forms.TimeField(required=True)

    pax = forms.ChoiceField(choices=(), required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        self.club = kwargs.pop('club', None)
        self.rates = kwargs.pop('rates', None)

        super(GolfClubBookingForm, self).__init__(*args, **kwargs)

        self.fields['pax'].choices = tuple((str(i), str(i)) for i in [x for x in range(1, int(self.club.max_pax) + 1)])

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

        if int(data) < 1 or int(data) > self.club.max_pax:
            raise forms.ValidationError(_('Invalid PAX'))

        return data

    def clean(self):
        super().clean()

        if not self.request.user.is_authenticated or not self.request.user.groups.filter(name='customers').exists():
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

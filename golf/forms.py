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
        super(GolfClubBookingForm, self).__init__(*args, **kwargs)

    class Meta:
        model = models.Order
        fields = []


class SearchForm(forms.Form):
    q = forms.CharField(
        label=_('search word'),
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

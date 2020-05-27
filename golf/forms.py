from django import forms
from django.utils.translation import gettext_lazy as _


class GolfClubBookingForm(forms.Form):
    round_date = forms.DateField()

    round_time = forms.TimeField()

    pax = forms.IntegerField()

    # TODO: Validation rules


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

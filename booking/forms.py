from django import forms
from django.utils import timezone
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
        self.holidays = kwargs.pop('holidays', None)

        self.now = timezone.datetime.now()

        super(GolfClubBookingForm, self).__init__(*args, **kwargs)

        self.fields['pax'].choices = tuple((str(i), str(i)) for i in [x for x in range(1, int(self.club.max_pax) + 1)])

    class Meta:
        model = models.Order
        fields = []

    def clean_round_date(self):
        data = self.cleaned_data['round_date']

        if (self.now + timezone.timedelta(days=1)).replace(hour=0, minute=0, second=0, microsecond=0) > \
                self.now > \
                self.now.replace(hour=16, minute=0, second=0, microsecond=0):
            if data < \
                    timezone.datetime.date(self.now + timezone.timedelta(self.club.weekdays_min_in_advance + 1)) \
                    or data > \
                    timezone.datetime.date(self.now + timezone.timedelta(self.club.weekdays_max_in_advance + 1)):
                raise forms.ValidationError(_('Invalid round date'))
        else:
            if data < \
                    timezone.datetime.date(self.now + timezone.timedelta(self.club.weekdays_min_in_advance)) \
                    or data > \
                    timezone.datetime.date(self.now + timezone.timedelta(self.club.weekdays_max_in_advance)):
                raise forms.ValidationError(_('Invalid round date'))

        return data

    def clean_round_time(self):
        data = self.cleaned_data['round_time']

        if data < timezone.datetime.strptime('06:00', '%H:%M').time() \
                or data > timezone.datetime.strptime('10:30', '%H:%M').time():
            raise forms.ValidationError(_('Invalid round time'))

        return data

    def clean_pax(self):
        data = self.cleaned_data['pax']

        if int(data) < 1 or int(data) > self.club.max_pax:
            raise forms.ValidationError(_('Invalid PAX'))

        return data

    def clean(self):
        super().clean()

        self.cleaned_data['club'] = self.club

        # 1. Authentication and Group membership
        if not self.request.user.is_authenticated or not self.request.user.groups.filter(name='customers').exists():
            raise forms.ValidationError(_('You have to sign in as a customer for booking.'))

        # 2. Green fee validation

        # 2.1. Weekday
        holiday = 1 if self.cleaned_data['round_date'].weekday() in [5, 6] else 0

        for day in self.holidays:
            if day.holiday > self.cleaned_data['round_date']:
                break
            elif day.holiday == self.cleaned_data['round_date']:
                holiday = 1
                break

        # 2.2 Rate
        if not holiday \
                or (holiday
                    and self.cleaned_data['round_date'] - timezone.datetime.date(self.now)
                    < timezone.timedelta(days=self.club.weekend_max_in_advance)):
            for rate in self.rates:
                if rate.day_of_week == holiday \
                        and rate.season_end >= self.cleaned_data['round_date'] >= rate.season_start \
                        and rate.slot_end >= self.cleaned_data['round_time'] >= rate.slot_start:
                    self.cleaned_data['green_fee_selling_price'] = rate.green_fee_selling_price
                    self.cleaned_data['green_fee_cost_price'] = rate.green_fee_cost_price

                    self.cleaned_data['total_selling_price'] = rate.green_fee_selling_price \
                                                               * int(self.cleaned_data['pax'])
                    self.cleaned_data['total_cost_price'] = rate.green_fee_cost_price \
                                                            * int(self.cleaned_data['pax'])
                    return

        raise forms.ValidationError(_('Invalid date, time or PAX'))


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

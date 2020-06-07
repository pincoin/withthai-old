from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('',
         views.GolfClubListView.as_view(), name='golf-club-list'),

    path('area/<slug:slug>/',
         views.GolfAreaListView.as_view(), name='golf-area-list'),

    path('province/<slug:slug>/',
         views.GolfProvinceListView.as_view(), name='golf-province-list'),

    path('club/<slug:slug>/',
         views.GolfClubBookingForm.as_view(), name='golf-club-booking'),

    path('club/<slug:slug>.json',
         views.GolfClubBookingJson.as_view(), name='golf-club-booking-json'),
]

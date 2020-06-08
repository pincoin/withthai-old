from django.urls import path

from . import views

app_name = 'booking'

urlpatterns = [
    path('golf/',
         views.GolfClubListView.as_view(), name='golf-club-list'),

    path('golf/area/<slug:slug>/',
         views.GolfAreaListView.as_view(), name='golf-area-list'),

    path('golf/province/<slug:slug>/',
         views.GolfProvinceListView.as_view(), name='golf-province-list'),

    path('golf/<slug:slug>/',
         views.GolfClubBookingCreateView.as_view(), name='golf-club-booking'),

    path('golf/<slug:slug>.json',
         views.GolfClubBookingJson.as_view(), name='golf-club-booking-json'),

    path('orders/',
         views.GolfClubListView.as_view(), name='order-list'),

    path('favorites/',
         views.GolfClubListView.as_view(), name='favorite-list'),
]

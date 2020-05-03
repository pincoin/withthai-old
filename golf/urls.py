from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    path('',
         views.GolfClubListView.as_view(), name='golf-club-list'),

    path('<slug:slug>/',
         views.GolfClubListView.as_view(), name='golf-club-detail'),
]

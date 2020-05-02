from django.urls import path

from . import views

app_name = 'golf'

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    path('<slug:slug>/',
         views.HomeView.as_view(), name='club-detail'),
]

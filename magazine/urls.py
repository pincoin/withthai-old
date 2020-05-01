from django.urls import (
    path, re_path
)

from . import views

app_name = 'magazine'

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),
]

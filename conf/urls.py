from django.contrib import admin
from django.urls import (
    path, include
)

from . import views

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    path('accounts/',
         include('allauth.urls')),

    path('admin/',
         admin.site.urls),
]

from django.contrib import admin
from django.urls import (
    path, include
)

from . import views

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    path('help/',
         include('help.urls', namespace='help')),

    path('board/',
         include('board.urls', namespace='board')),

    path('magazine/',
         include('magazine.urls', namespace='magazine')),

    path('golf/',
         include('golf.urls', namespace='golf')),

    path('member/',
         include('member.urls', namespace='member')),

    path('accounts/',
         include('allauth.urls')),

    path('admin/',
         admin.site.urls),

    path('i18n/',
         include('django.conf.urls.i18n')),
]

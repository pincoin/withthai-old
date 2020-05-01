from django.urls import (
    path, re_path
)

from . import views

app_name = 'golf'

urlpatterns = [
    path('',
         views.HomeView.as_view(), name='home'),

    re_path(r'^(?P<slug>[-\w]+)/$',
            views.HomeView.as_view(), name='club-detail'),
]

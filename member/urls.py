from django.urls import path

from . import views

app_name = 'member'

urlpatterns = [
    path('social-signup-test',
         views.SocialSignUpTestView.as_view(), name='social-sign-up-test-view'),
]

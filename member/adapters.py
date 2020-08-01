from allauth.account.adapter import DefaultAccountAdapter
from allauth.socialaccount.adapter import DefaultSocialAccountAdapter

from django.urls import reverse


class MyAccountAdapter(DefaultAccountAdapter):
    def is_open_for_signup(self, request):
        if request.path.rstrip('/') == reverse('account_signup').rstrip('/'):
            return False
        return True


class SocialAccountAdapter(DefaultSocialAccountAdapter):
    pass

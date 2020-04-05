import json
import os

from . import BASE_DIR

# Secret settings
secret = json.loads(open(os.path.join(BASE_DIR, 'secret.json')).read())

SECRET_KEY = secret['SECRET_KEY']
ALLOWED_HOSTS = secret['ALLOWED_HOSTS']
DATABASES = secret['DATABASES']
DEBUG = secret['DEBUG']

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
]

INSTALLED_APPS += [
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.facebook',
    'allauth.socialaccount.providers.google',
    'allauth.socialaccount.providers.kakao',
    'allauth.socialaccount.providers.naver',
    'member.socialaccount.providers.line',
]

INSTALLED_APPS += [
    'member',
    'blog',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'conf.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'conf', 'templates'),
            os.path.join(BASE_DIR, 'allauth', 'templates'),
            os.path.join(BASE_DIR, 'blog', 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'conf.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator', },
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', },
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator', },
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator', },
]

AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)

SITE_ID = 1

# django.contrib.auth settings for allauth
PASSWORD_RESET_TIMEOUT_DAYS = 1  # default=3
LOGIN_URL = '/accounts/login/'  # default=/accounts/login/
LOGOUT_URL = '/accounts/logout/'  # default=/accounts/logout/
LOGIN_REDIRECT_URL = '/shop/default'  # default=/accounts/profile/
# LOGOUT_REDIRECT_URL = '/'

# django-allauth
# DEFAULT_FROM_EMAIL = secret.EMAIL_NO_REPLY
# ACCOUNT_ADAPTER = 'member.adapters.MyAccountAdapter'
ACCOUNT_AUTHENTICATION_METHOD = 'email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_VERIFICATION = 'mandatory'
ACCOUNT_LOGIN_ATTEMPTS_LIMIT = 5
ACCOUNT_LOGIN_ATTEMPTS_TIMEOUT = 300
# ACCOUNT_SIGNUP_FORM_CLASS = 'member.forms.MemberSignupForm'
ACCOUNT_LOGOUT_ON_PASSWORD_CHANGE = True  # default=False
SOCIALACCOUNT_AUTO_SIGNUP = False

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {},
    'google': {},
    'kakao': {},
    'naver': {},
    'line': {
        'SCOPE': [
            'profile',
            'openid',
            'email',
        ],
    },
}

from django.utils.translation import ugettext_lazy as _

from .base import *

# Internationalization
LANGUAGE_CODE = 'ko-KR'
LANGUAGES = [
    ('ko', _('Korean')),
    ('th', _('Thai')),
    ('en', _('English')),
]
LOCALE_PATHS = (
    os.path.join(BASE_DIR, 'locale'),
)
USE_I18N = True
USE_L10N = True
USE_TZ = True
TIME_ZONE = 'Asia/Bangkok'

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/assets/'
STATIC_ROOT = os.path.join(BASE_DIR, 'assets/')
STATICFILES_DIRS = [
    '/Users/mairoo/.pyenv/versions/toj/lib/python3.6/site-packages/django/contrib/admin/static',
    os.path.join(BASE_DIR, 'conf', 'static'),
]
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    #'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)

# Media files (Uploaded files)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media/')

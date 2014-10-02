"""
Django settings for demo project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

def rel_base(*x):
    return os.path.join(BASE_DIR, *x)

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'st*+e@o(kp8&gvms(e1^sd=!5-%f^)uziaxz#3!0k_bzu%44ys'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = (
    'django.contrib.sessions',
    'django.contrib.staticfiles',

    'compressor',
    'storages',

    'pages',
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'demo.urls'

WSGI_APPLICATION = 'demo.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


AWS_ACCESS_KEY_ID = None  # secrets.py
AWS_SECRET_ACCESS_KEY = None  # secrets.py
AWS_IS_GZIPPED = False
AWS_QUERYSTRING_AUTH = False
AWS_S3_FILE_OVERWRITE = False

STATIC_URL = '/static/'
STATIC_ROOT = rel_base('assets/')
STATIC_BUCKET = None
STATIC_LOCATION = None
STATIC_DOMAIN = None
STATIC_HEADERS = {
    'Expires': 'Thu, 31 Dec 2050 00:00:00 GMT',
    'Cache-Control': 'max-age=315360000, public',
}
STATICFILES_DIRS = (
    rel_base('static/'),
)
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    'compressor.finders.CompressorFinder',
)

COMPRESS_ENABLED = True
COMPRESS_OUTPUT_DIR = '.'
COMPRESS_PRECOMPILERS = (
    ('text/x-scss', 'core.precompilers.ScssFilter'),
)


TEMPLATE_DIRS = (
    rel_base('templates/'),
)

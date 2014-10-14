from .base import *  # noqa

DEBUG = False
TEMPLATE_DEBUG = False

ALLOWED_HOSTS = ['*']


# Use memcached
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'default'
    },
    'staticfiles': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': 'staticfiles'
    }
}


# STATIC_URL = 'https://d5676rztcqm37.cloudfront.net/static/'
STATIC_URL = 'https://sophilabs-compressor.s3.amazonaws.com/static/'
STATIC_BUCKET = 'sophilabs-compressor'
STATIC_LOCATION = 'static'
# STATIC_DOMAIN = 'd5676rztcqm37.cloudfront.net'
STATIC_DOMAIN = 'sophilabs-compressor.s3.amazonaws.com'
STATICFILES_STORAGE = 'core.storages.StaticStorage'

COMPRESS_ENABLED = True
# COMPRESS_URL = 'https://d5676rztcqm37.cloudfront.net/static/'
COMPRESS_URL = 'https://sophilabs-compressor.s3.amazonaws.com/static/'
COMPRESS_ROOT = STATIC_ROOT
COMPRESS_STORAGE  = 'core.storages.CompressorStorage'
COMPRESS_CACHE_BACKEND = 'staticfiles'
COMPRESS_CSS_FILTERS = []


LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'level': 'INFO',
            'class': 'logging.StreamHandler',
        },
        'null': {
            'class': 'logging.NullHandler',
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django': {
            'handlers': ['console'],
        },
        'django.request': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'django.security': {
            'handlers': ['console'],
            'level': 'ERROR',
            'propagate': False,
        },
        'py.warnings': {
            'handlers': ['console'],
        },
    }
}

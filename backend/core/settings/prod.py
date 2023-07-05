"""
Configuration for deployment to Fly.io / Heroku with Dockerfile.(fly/heroku)
"""
import dj_database_url

from core.settings.base import *

ROOT_DIR = BASE_DIR.parent.parent

SECRET_KEY = os.environ['SECRET_KEY']

PRODUCTION_HOST = os.environ['PRODUCTION_HOST']

ALLOWED_HOSTS = [
    PRODUCTION_HOST,
]

DEBUG = False

# cors headers configuration
# https://pypi.org/project/django-cors-headers/

CORS_ALLOW_ALL_ORIGINS = False

CORS_EXPOSE_HEADERS = [
    'Content-Disposition',
]

CORS_ORIGIN_WHITELIST = [
    origin for origin in os.getenv('CORS_ORIGIN_WHITELIST', '').split(',') if origin
]

# static files configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#static-files
# https://whitenoise.readthedocs.io/en/latest/

# whitenoise middle - has to be first in the list
MIDDLEWARE.insert(3, 'whitenoise.middleware.WhiteNoiseMiddleware')

# directories with templates or html files
TEMPLATES[0]['DIRS'] = [
    os.path.join(ROOT_DIR, 'frontend', 'build')
]

# directory where Django can find html, js, css, and other static assets
STATICFILES_DIRS = [
    os.path.join(ROOT_DIR, 'frontend', 'build', 'assets')
]

# directory where WhiteNoise can find all non-html static assets
WHITENOISE_ROOT = os.path.join(ROOT_DIR, 'frontend', 'build')

# type of static files storage
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')

STATIC_URL = '/static/'

# Database config
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASE_URL = os.environ['DATABASE_URL']

db_from_env = dj_database_url.config(
    default=DATABASE_URL,
    conn_max_age=500,
    conn_health_checks=True,
    ssl_require=True
)

DATABASES['default'].update({
    **db_from_env,
    'ENGINE': 'django.db.backends.postgresql',
    'OPTIONS': {
        'connect_timeout': 5,
    }
})

# Django cache config
# https://docs.djangoproject.com/en/4.2/ref/settings/#caches

REDIS_URL = os.environ['REDIS_URL']

CACHES = {
    "default": {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': REDIS_URL,
    }
}

# Django Channels config
# https://channels.readthedocs.io/en/stable/deploying.html#setting-up-a-channel-backend

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                REDIS_URL
            ],
        },
    },
}

# Django-Q config
# https://django-q.readthedocs.io/en/latest/configure.html

Q_CLUSTER = {
    'name': 'beerdegu_cluster',
    'workers': 8,
    'recycle': 500,
    'timeout': 60,
    'compress': True,
    'save_limit': 250,
    'queue_limit': 500,
    'cpu_affinity': 1,
    'label': 'Django Q',
    'redis': REDIS_URL
}

# dj-rest-auth, django-all-auth config
# https://django-allauth.readthedocs.io/en/latest/configuration.html
# https://dj-rest-auth.readthedocs.io/en/latest/configuration.html

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

# Emails config
# https://docs.djangoproject.com/en/4.2/topics/email/#smtp-backend

EMAIL_BACKEND = 'core.shared.email_backend.DjangoQBackend'
DJANGO_Q_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_USE_TLS = True

CSRF_TRUSTED_ORIGINS = [
    f'https://{PRODUCTION_HOST}'
]

"""
Configuration for production deployment (heroku/fly/railway).
"""
import dj_database_url

from core.settings.base import *

ROOT_DIR = BASE_DIR.parent

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

CORS_ORIGIN_REGEX_WHITELIST = [
    fr'{origin}' for origin in os.getenv('CORS_ORIGIN_REGEX_WHITELIST', '').split(',') if origin
]

# Django static files configuration
# https://docs.djangoproject.com/en/4.2/ref/settings/#static-files

# Whitenoise configuration
# https://whitenoise.readthedocs.io/en/latest/

# AWS S3 configuration
# https://testdriven.io/blog/storing-django-static-and-media-files-on-amazon-s3/
# https://django-storages.readthedocs.io/en/latest/backends/amazon-S3.html

USE_AWS_S3 = os.getenv('USE_S3', 'FALSE').lower() == 'true'

if USE_AWS_S3:
    # aws settings
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': f'max-age={24 * 3600}'}

    # s3 static settings
    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

    # s3 public media settings
    PUBLIC_MEDIA_LOCATION = 'uploads'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    MEDIA_ROOT = None

    STORAGES = {
        # to allow media upload to s3
        'default': {
            'BACKEND': 'core.shared.storages.PublicMediaStorage'
        },
        # to allow `collectstatic to s3
        'staticfiles': {
            'BACKEND': 'core.shared.storages.StaticStorage'
        },
    }
else:
    MIDDLEWARE.insert(3, 'whitenoise.middleware.WhiteNoiseMiddleware')

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(ROOT_DIR, 'staticfiles')

    STORAGES = {
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        }
    }

    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(ROOT_DIR, 'uploads')

if SERVE_FRONTEND:
    WHITENOISE_ROOT = os.path.join(ROOT_DIR, 'frontend', 'build')
    STATICFILES_DIRS = [
        os.path.join(ROOT_DIR, 'frontend', 'build', 'assets')
    ]
    TEMPLATES[0]['DIRS'] = [
        os.path.join(ROOT_DIR, 'frontend', 'build')
    ]

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

# Rest framework
# https://www.django-rest-framework.org/api-guide/settings/

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

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
    'workers': int(os.getenv('Q_CLUSTER_WORKERS', 4)),
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

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

CSRF_TRUSTED_ORIGINS = [
    f'https://{PRODUCTION_HOST}'
]

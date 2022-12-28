"""
Configuration for deployment to Heroku with Dockerfile.prod
"""
import os

import dj_database_url
from core.settings.base import *

# project directory
ROOT_DIR = BASE_DIR.parent.parent

# set SECRET_KEY for production
SECRET_KEY = os.environ["SECRET_KEY"]

# add heroku app url or create env var with url
ALLOWED_HOSTS = [
    os.environ["PRODUCTION_HOST"]
]

# debug has to be false in production
DEBUG = False

# cors headers configuration
CORS_ALLOW_ALL_ORIGINS = False
CORS_EXPOSE_HEADERS = [
    'Content-Disposition',
]

INSTALLED_APPS.extend(["whitenoise.runserver_nostatic"])

# whitenoise middle - has to be first in the list
MIDDLEWARE.insert(1, "whitenoise.middleware.WhiteNoiseMiddleware")

# directories with templates or html files
TEMPLATES[0]["DIRS"] = [os.path.join(ROOT_DIR, "frontend", "build")]

# directory where Django can find html, js, css, and other static assets
STATICFILES_DIRS = [os.path.join(ROOT_DIR, "frontend", "build", "assets")]

# type of static files storage
STATICFILES_STORAGE = "whitenoise.storage.CompressedManifestStaticFilesStorage"

STATIC_ROOT = os.path.join(ROOT_DIR, "staticfiles")

STATIC_URL = "/static/"

# directory where WhiteNoise can find all non-html static assets
WHITENOISE_ROOT = os.path.join(ROOT_DIR, "frontend", "build")

# database url set at env variable in Heroku
DATABASE_URL = os.environ['DATABASE_URL']

# db config
db_from_env = dj_database_url.config(
    default=DATABASE_URL, conn_max_age=500, ssl_require=True
)

DATABASES['default'].update(db_from_env)

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [os.environ['REDIS_URL']],
        },
    },
}

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
    "redis": os.environ['REDIS_URL']
}

ACCOUNT_DEFAULT_HTTP_PROTOCOL = "https"

EMAIL_BACKEND = 'core.shared.email_backend.DjangoQBackend'
DJANGO_Q_EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'

EMAIL_HOST = os.environ['EMAIL_HOST']
EMAIL_PORT = int(os.environ['EMAIL_PORT'])
EMAIL_HOST_USER = os.environ['EMAIL_USER']
EMAIL_HOST_PASSWORD = os.environ['EMAIL_PASSWORD']
EMAIL_USE_TLS = True

CSRF_TRUSTED_ORIGINS = [
    f'https://{os.environ["PRODUCTION_HOST"]}'
]

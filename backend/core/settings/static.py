"""
Configuration for collecting static files in production.
Do not use as runtime settings. Server should be running with `core.settings.prod`!
"""
from django.core.management.utils import get_random_secret_key

from core.settings.base import *

ALLOWED_HOSTS = []

ROOT_DIR = BASE_DIR.parent

SECRET_KEY = get_random_secret_key()

DEBUG = False

USE_AWS_S3 = os.getenv('USE_S3', 'FALSE').lower() == 'true'

if USE_AWS_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {'CacheControl': f'max-age={24 * 3600}'}

    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

    PUBLIC_MEDIA_LOCATION = 'uploads'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'
    MEDIA_ROOT = None

    STORAGES = {
        'default': {
            'BACKEND': 'core.shared.storages.PublicMediaStorage'
        },
        'staticfiles': {
            'BACKEND': 'core.shared.storages.StaticStorage'
        },
    }
else:
    MIDDLEWARE.insert(3, 'whitenoise.middleware.WhiteNoiseMiddleware')

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    STORAGES = {
        'staticfiles': {
            'BACKEND': 'whitenoise.storage.CompressedManifestStaticFilesStorage',
        }
    }

    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

if SERVE_FRONTEND:
    WHITENOISE_ROOT = os.path.join(ROOT_DIR, 'frontend', 'build')
    STATICFILES_DIRS = [
        os.path.join(ROOT_DIR, 'frontend', 'build', 'assets')
    ]
    TEMPLATES[0]['DIRS'] = [
        os.path.join(ROOT_DIR, 'frontend', 'build')
    ]

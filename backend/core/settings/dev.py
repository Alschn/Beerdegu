"""
Configuration for development with Docker.
"""
from core.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'development')

DEBUG = True

ALLOWED_HOSTS = ['backend', 'localhost', '127.0.0.1', 'host.docker.internal', '*']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'postgres_db'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

USE_AWS_S3 = os.getenv('USE_AWS_S3', 'FALSE').lower() == 'true'

if USE_AWS_S3:
    AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
    AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
    AWS_STORAGE_BUCKET_NAME = os.getenv('AWS_STORAGE_BUCKET_NAME')
    AWS_DEFAULT_ACL = None
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    AWS_S3_OBJECT_PARAMETERS = {
        'CacheControl': f'max-age={24 * 3600}'
    }

    STATIC_LOCATION = 'static'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{STATIC_LOCATION}/'

    PUBLIC_MEDIA_LOCATION = 'uploads'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/{PUBLIC_MEDIA_LOCATION}/'

    STORAGES = {
        "default": {
            "BACKEND": "core.shared.storages.PublicMediaStorage"
        },
        "staticfiles": {
            "BACKEND": "core.shared.storages.StaticStorage"
        },
    }
else:
    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

    MEDIA_URL = '/uploads/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'uploads')

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis_db')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.redis.RedisCache',
        'LOCATION': f'redis://{REDIS_HOST}:{REDIS_PORT}',
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            'hosts': [
                (
                    REDIS_HOST,
                    REDIS_PORT
                )
            ],
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
    'redis': {
        'host': REDIS_HOST,
        'port': REDIS_PORT,
        'db': 0,
    }
}

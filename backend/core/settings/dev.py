"""
Configuration for development with Docker.
"""
from core.settings.base import *

SECRET_KEY = os.environ.get('SECRET_KEY', 'development')

DEBUG = True

ALLOWED_HOSTS = ['backend', 'localhost', '127.0.0.1', 'host.docker.internal']

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

REDIS_HOST = os.environ.get('REDIS_HOST', 'redis_db')
REDIS_PORT = os.environ.get('REDIS_PORT', 6379)

CACHES = {
    "default": {
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

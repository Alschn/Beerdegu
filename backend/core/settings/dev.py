"""
Configuration for development with Docker.
"""
from core.settings.base import *

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'development')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ["backend", "localhost", "127.0.0.1"]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.environ.get('DB_NAME', 'postgres'),
        'USER': os.environ.get('DB_USER', 'postgres'),
        'PASSWORD': os.environ.get('DB_PASSWORD', 'postgres'),
        'HOST': os.environ.get('DB_HOST', 'db'),
        'PORT': os.environ.get('DB_PORT', 5432),
    }
}

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels_redis.core.RedisChannelLayer',
        'CONFIG': {
            "hosts": [
                (
                    # redis_db = service's name
                    os.environ.get('REDIS_HOST', 'redis_db'),
                    os.environ.get('REDIS_PORT', 6379)
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
    "redis": {
        'host': os.environ.get('REDIS_HOST', 'redis_db'),
        'port': os.environ.get('REDIS_PORT', 6379),
        'db': 0,
    }
}

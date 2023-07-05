"""
Django settings for backend project.

Generated by 'django-admin startproject' using Django 3.2.2.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
import os
from datetime import timedelta
from pathlib import Path

from dotenv import load_dotenv

# Load environmental variables
load_dotenv()

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY', 'development_without_docker')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['backend', 'localhost', '127.0.0.1', 'host.docker.internal']

# Application definition
INSTALLED_APPS = [
    # django channels
    'channels',
    # django packages
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    # django utils
    'django_extensions',
    'django_filters',
    'import_export',
    # task queue
    'django_q',
    # cors headers
    'corsheaders',
    # rest framework
    'rest_framework',
    # simplejwt
    'rest_framework_simplejwt',
    'rest_framework_simplejwt.token_blacklist',
    # auth
    'dj_rest_auth',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'dj_rest_auth.registration',
    # social auth
    'allauth.socialaccount.providers.google',
    # open api schema
    'drf_spectacular',
    # apps
    'core',
    'users',
    'rooms',
    'beers',
]

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    # 'django.middleware.locale.LocaleMiddleware'   # todo: in future
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    # 'users.middleware.AccessCookieToAuthorizationHeaderMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

CHANNEL_LAYERS = {
    'default': {
        'BACKEND': 'channels.layers.InMemoryChannelLayer'
    }
}

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

# GitHub actions database
if os.environ.get('GITHUB_WORKFLOW'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': 'github_actions',
            'USER': 'postgres',
            'PASSWORD': 'postgres',
            'HOST': '127.0.0.1',
            'PORT': '5432',
        }
    }
# SQLite database if not using Docker for development
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR.parent, 'db.sqlite3'),
        }
    }

# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/
# https://www.django-rest-framework.org/topics/internationalization/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Warsaw'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Rest Framework config - Authentication, filtering...
# https://www.django-rest-framework.org/api-guide/settings/

AUTHENTICATION_CLASSES_DEBUG = (
    'rest_framework.authentication.SessionAuthentication',
    'rest_framework.authentication.BasicAuthentication',
) if DEBUG else ()

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': (
        ('rest_framework.permissions.AllowAny',)
    ),

    'DEFAULT_AUTHENTICATION_CLASSES': (
        *AUTHENTICATION_CLASSES_DEBUG,
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),

    'DEFAULT_FILTER_BACKENDS': (
        'django_filters.rest_framework.DjangoFilterBackend',
    ),

    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
}

# Authentication backends
# https://django-allauth.readthedocs.io/en/latest/configuration.html

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'sesame.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
]

# JWT settings
# https://django-rest-framework-simplejwt.readthedocs.io/en/latest/settings.html

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(hours=2),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ROTATE_REFRESH_TOKENS': False,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),

    'ALGORITHM': 'HS256',
    'JTI_CLAIM': 'jti',
    'USER_ID_CLAIM': 'user_id',
    'USER_ID_FIELD': 'id',

    # custom settings related to jwt
    'ACCESS_TOKEN_COOKIE': 'access',
    'REFRESH_TOKEN_COOKIE': 'refresh',
    # toggle if using cookies for JWT
    'SHOULD_SET_COOKIES': False,
}

# needed only if using cookies for JWT
COOKIE_DOMAIN = os.environ.get('COOKIE_DOMAIN', 'localhost')

# django-allauth settings
# https://django-allauth.readthedocs.io/en/latest/configuration.html

ACCOUNT_EMAIL_VERIFICATION = 'none'
ACCOUNT_DEFAULT_HTTP_PROTOCOL = 'http'
OLD_PASSWORD_FIELD_ENABLED = True

# dj-rest-auth settings
# https://dj-rest-auth.readthedocs.io/en/latest/configuration.html#token-model

REST_AUTH = {
    'TOKEN_MODEL': None
}

# drf-spectacular settings
# https://drf-spectacular.readthedocs.io/en/latest/settings.html

SPECTACULAR_SETTINGS = {
    'TITLE': 'Beerdegu API',
    'DESCRIPTION': 'Beerdegu API provided by Alschn',
    'VERSION': '1.0.0',
    'CONTACT': {
        'name': 'Alschn',
        'url': 'https://github.com/Alschn/',
    },
    'SERVE_PERMISSIONS': ['rest_framework.permissions.AllowAny'],
}

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/
STATIC_URL = '/static/'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS headers
CORS_ALLOW_ALL_ORIGINS = True
CORS_EXPOSE_HEADERS = [
    'Content-Disposition',
]

# required by django.contrib.sites
SITE_ID = 1

# Django Q configuration
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
    # if not using Docker, you have to run Redis server by yourself
    'redis': {
        'host': '127.0.0.1',
        'port': 6379,
        'db': 0,
    }
}

# https://docs.djangoproject.com/en/4.0/ref/settings/#csrf-trusted-origins

CSRF_TRUSTED_ORIGINS = [
    'http://127.0.0.1'
]

# Sending emails (+ Django Q integration)
# https://docs.djangoproject.com/en/4.0/topics/email/

EMAIL_BACKEND = 'core.shared.email_backend.DjangoQBackend'
DJANGO_Q_EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

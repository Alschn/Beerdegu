from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from storages.backends.s3boto3 import S3Boto3Storage

if not settings.USE_AWS_S3:
    raise ImproperlyConfigured('You need to set `USE_AWS_S3 = True` in settings to use storages from this file.')


class StaticStorage(S3Boto3Storage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3Boto3Storage):
    location = 'uploads'
    default_acl = 'public-read'
    file_overwrite = False

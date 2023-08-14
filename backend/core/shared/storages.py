from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from storages.backends.s3boto3 import S3ManifestStaticStorage

if not settings.USE_AWS_S3:
    raise ImproperlyConfigured('You need to set `USE_AWS_S3 = True` in settings to use storages from this file.')


class StaticStorage(S3ManifestStaticStorage):
    location = 'static'
    default_acl = 'public-read'


class PublicMediaStorage(S3ManifestStaticStorage):
    location = 'uploads'
    default_acl = 'public-read'
    file_overwrite = False

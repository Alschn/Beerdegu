from django.conf import settings
from django.contrib.sites.models import Site
from django.core.exceptions import ImproperlyConfigured


def get_frontend_site() -> Site:
    name = settings.FRONTEND_SITE_NAME

    if not name:
        raise ImproperlyConfigured(
            'FRONTEND_SITE_NAME must be set in settings.py.'
        )

    try:
        return Site.objects.get(name=name)
    except Site.DoesNotExist:
        raise ImproperlyConfigured(
            f'Could not find site named `{name}` in Site objects.'
        )


def get_frontend_domain() -> str:
    site_frontend = get_frontend_site()
    domain = site_frontend.domain

    if not (domain.startswith('http') or domain.startswith('https')):
        raise ImproperlyConfigured(
            f'Site `{site_frontend.name}` domain must start with `http://` or `https://`. Got `{domain}`.'
        )

    if domain.endswith('/'):
        domain = domain[:-1]

    return domain


def build_frontend_url(path: str) -> str:
    domain = get_frontend_domain()
    if not path.startswith('/'):
        path = '/' + path
    return domain + path

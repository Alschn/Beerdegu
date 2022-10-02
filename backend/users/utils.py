from typing import TypedDict

from django.conf import settings
from rest_framework_simplejwt.tokens import RefreshToken

ACCESS_COOKIE_MAX_AGE = settings.SIMPLE_JWT['ACCESS_TOKEN_LIFETIME'].total_seconds()
REFRESH_COOKIE_MAX_AGE = settings.SIMPLE_JWT['REFRESH_TOKEN_LIFETIME'].total_seconds()
ACCESS_TOKEN_KEY = settings.SIMPLE_JWT['ACCESS_TOKEN_COOKIE']
REFRESH_TOKEN_KEY = settings.SIMPLE_JWT['REFRESH_TOKEN_COOKIE']


def get_tokens_for_user(user) -> tuple[str, str]:
    """
    Returns access and refresh token pair.
    access, refresh = get_tokens_for_user(user)
    """
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token), str(refresh)


class SetCookieArguments(TypedDict):
    key: str  # Literal['access', 'refresh']
    value: str
    max_age: str | int
    expires: str | int
    secure: bool
    httponly: bool
    samesite: str  # Literal['None', 'Lax', 'Strict']
    domain: str


def get_set_cookie_args(token: str, is_access: bool = True, **kwargs) -> SetCookieArguments:
    """Returns dict with arguments passed to set_cookie function."""

    # token can either be access or refresh
    max_age = ACCESS_COOKIE_MAX_AGE if is_access else REFRESH_COOKIE_MAX_AGE
    key = ACCESS_TOKEN_KEY if is_access else REFRESH_TOKEN_KEY

    return {
        "key": key,
        "value": token,
        "max_age": max_age,
        "expires": max_age,
        "secure": not settings.DEBUG,
        "httponly": True,
        "samesite": "None" if not settings.DEBUG else "Lax",
        "domain": settings.COOKIE_DOMAIN,
        **kwargs
    }


def get_delete_cookie_args(is_access: bool = True, **kwargs) -> SetCookieArguments:
    """Returns dict with arguments passed to set_cookie function.
    Set_cookie with those arguments behaves like delete_cookie under the hood."""

    return {
        "key": ACCESS_TOKEN_KEY if is_access else REFRESH_TOKEN_KEY,
        "value": "",
        "max_age": 0,
        "expires": 'Thu, 01 Jan 1970 00:00:00 GMT',
        "secure": not settings.DEBUG,
        "httponly": True,
        "samesite": "None" if not settings.DEBUG else "Lax",
        "domain": settings.COOKIE_DOMAIN,
        **kwargs
    }

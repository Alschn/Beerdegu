from typing import Callable, Any

from rest_framework.request import Request

from users.utils import ACCESS_TOKEN_KEY


class AccessCookieToAuthorizationHeaderMiddleware:
    """Intercepts request and injects 'access' cookie into HTTP_AUTHORIZATION header"""

    def __init__(self, get_response: Callable = None):
        self.get_response = get_response

    def __call__(self, request: Request, *args: Any, **kwargs: Any):
        access_token = request.COOKIES.get(ACCESS_TOKEN_KEY)

        if access_token:
            request.META['HTTP_AUTHORIZATION'] = f'Bearer {access_token}'

        return self.get_response(request)

from typing import Any

from django.conf import settings
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework_simplejwt.views import TokenObtainPairView

from users.serializers.auth import TokenObtainPairSerializer
from users.utils import (
    get_set_cookie_args, ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
)


class JWTObtainPairView(TokenObtainPairView):
    """
    POST /api/auth/token/
    """
    serializer_class = TokenObtainPairSerializer

    def finalize_response(self, request: Request, response: Response, *args: Any, **kwargs: Any) -> Response:
        """Sets cookies for access and refresh tokens after having processed the response."""

        should_set_cookies = settings.SIMPLE_JWT.get('SHOULD_SET_COOKIES', False)

        if not should_set_cookies or response.status_code != HTTP_200_OK:
            return super().finalize_response(request, response, *args, **kwargs)

        access = response.data.get(ACCESS_TOKEN_KEY)
        refresh = response.data.get(REFRESH_TOKEN_KEY)
        response.set_cookie(**get_set_cookie_args(token=access))
        response.set_cookie(**get_set_cookie_args(token=refresh, is_access=False))
        return super().finalize_response(request, response, *args, **kwargs)

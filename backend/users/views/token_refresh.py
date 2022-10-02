from typing import Any

from django.conf import settings
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenRefreshView

from users.serializers.auth import CookieTokenRefreshSerializer
from users.utils import (
    get_set_cookie_args, ACCESS_TOKEN_KEY, REFRESH_TOKEN_KEY
)


class JWTRefreshView(TokenRefreshView):
    """
    POST /api/auth/token/refresh/
    """
    serializer_class = CookieTokenRefreshSerializer

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        # if refresh cookie exists and refresh was not submitted via form/request
        if (refresh := request.COOKIES.get(REFRESH_TOKEN_KEY)) and not request.data.get('refresh'):
            data = dict(request.data)
            data.update({"refresh": str(refresh)})
            serializer = self.get_serializer(data=data)
        else:
            # default behaviour
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.validated_data, status=status.HTTP_200_OK)

    def finalize_response(self, request: Request, response: Response, *args: Any, **kwargs: Any) -> Response:
        """Sets cookies for access token after having processed the response."""

        if not settings.SIMPLE_JWT['SHOULD_SET_COOKIES']:
            return super().finalize_response(request, response, *args, **kwargs)

        if access := response.data.get(ACCESS_TOKEN_KEY):
            response.set_cookie(**get_set_cookie_args(token=access))

        return super().finalize_response(request, response, *args, **kwargs)

from dj_rest_auth.views import LogoutView
from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken
from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from users.utils import (
    get_delete_cookie_args, REFRESH_TOKEN_KEY, SHOULD_SET_COOKIES
)


class LogoutAPIView(LogoutView):
    """
    POST /api/auth/logout/
    """
    permission_classes = [IsAuthenticated]

    def logout(self, request) -> Response:
        # default behaviour from dj_rest_auth
        # since we support both Token and JWT authentication,
        # we need to all types of logout just in case

        try:
            request.user.auth_token.delete()
        except (AttributeError, ObjectDoesNotExist):
            pass

        # custom behaviour when using JWT authentication
        if not SHOULD_SET_COOKIES:
            refresh_tokens = OutstandingToken.objects.filter(user=request.user)
            for refresh in refresh_tokens:
                BlacklistedToken.objects.get_or_create(token=refresh)

        # default django logout to get rid of session, uncomment if needed
        # django_logout(request)

        # custom behaviour when cookies are enabled
        elif SHOULD_SET_COOKIES:
            return self.jwt_cookies_logout(request)

        return Response(
            {'message': 'Successfully logged out.'},
            status=status.HTTP_200_OK,
        )

    def jwt_cookies_logout(self, request) -> Response:
        if not (refresh := request.COOKIES.get(REFRESH_TOKEN_KEY)):
            # this is technically not an error - we cannot blacklist refresh token because it is missing,
            # but we can still make sure that there is no access token in client's browser
            # user could have manually removed refresh token and left access token
            response = Response(
                {'message': 'Cookie \'refresh\' not found in request!'},
                status=status.HTTP_204_NO_CONTENT
            )
            response.set_cookie(**get_delete_cookie_args())
            return response

        response = Response({'message': 'Logout successful!'}, status=status.HTTP_200_OK)

        # delete access cookie
        response.set_cookie(**get_delete_cookie_args())

        try:
            refresh_token = RefreshToken(refresh)
            refresh_token.blacklist()
        except TokenError:
            # if refresh token has already been blacklisted, then just delete refresh cookie
            pass

        # delete refresh cookie
        response.set_cookie(**get_delete_cookie_args(is_access=False))

        return response

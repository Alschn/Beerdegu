from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.exceptions import TokenError, InvalidToken
from rest_framework_simplejwt.views import TokenVerifyView

from users.serializers.auth import CookieTokenVerifySerializer
from users.utils import ACCESS_TOKEN_KEY


class JWTVerifyView(TokenVerifyView):
    """
    POST /api/auth/token/verify/
    """
    serializer_class = CookieTokenVerifySerializer

    def post(self, request: Request, *args, **kwargs) -> Response:
        # if access cookie exists and token was not submitted via form/request
        if (access := request.COOKIES.get(ACCESS_TOKEN_KEY)) and not request.data.get('token'):
            serializer = self.get_serializer(data={'token': str(access)})
        else:
            # default behaviour
            serializer = self.get_serializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
        except TokenError as e:
            raise InvalidToken(e.args[0])

        return Response(serializer.data, status=status.HTTP_200_OK)

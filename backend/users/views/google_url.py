import requests
from django.conf import settings
from rest_framework import status, serializers
from rest_framework.permissions import AllowAny
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

GOOGLE_AUTHORIZE_URL = 'https://accounts.google.com/o/oauth2/v2/auth'


class GoogleAuthURLSerializer(serializers.Serializer):
    # used only for open api schema generation
    url = serializers.URLField(read_only=True)


class GoogleAuthURLAPIView(APIView):
    """
    Returns url to google oauth2 authorization endpoint,
    which will be used by the frontend.
    """
    permission_classes = [AllowAny]
    serializer_class = GoogleAuthURLSerializer

    # noinspection PyMethodMayBeStatic
    def get(self, request: Request) -> Response:
        scopes = ' '.join(['openid', 'email', 'profile'])
        params = {
            'redirect_uri': settings.GOOGLE_CLIENT_REDIRECT_URI,
            'prompt': 'consent',
            'response_type': 'code',
            'client_id': settings.GOOGLE_CLIENT_ID,
            'scope': scopes,
            'access_type': 'offline'
        }
        req = requests.Request(
            'GET',
            GOOGLE_AUTHORIZE_URL,
            params=params
        )
        url = req.prepare().url
        return Response({'url': url}, status=status.HTTP_200_OK)

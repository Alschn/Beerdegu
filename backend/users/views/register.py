from dj_rest_auth.registration.views import RegisterView

from users.serializers.auth import RegisterUserSerializer


class RegisterAPIView(RegisterView):
    """
    POST /auth/register/
    """
    serializer_class = RegisterUserSerializer

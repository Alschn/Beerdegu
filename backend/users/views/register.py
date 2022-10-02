from dj_rest_auth.registration.views import RegisterView

from users.serializers.auth import RegisterUserSerializer
from users.serializers.user import UserSerializer


class RegisterAPIView(RegisterView):
    """
    POST /api/auth/register/
    """
    serializer_class = RegisterUserSerializer

    def get_response_data(self, user) -> dict:
        return UserSerializer(user).data

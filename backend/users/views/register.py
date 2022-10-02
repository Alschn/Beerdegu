from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
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

    def perform_create(self, serializer: RegisterUserSerializer):
        # behaviour from dj_rest_auth but without creating drf token
        user = serializer.save(request=self.request)

        complete_signup(
            self.request._request, user,
            allauth_settings.EMAIL_VERIFICATION,
            None,
        )
        return user

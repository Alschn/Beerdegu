from allauth.account import app_settings as allauth_settings
from allauth.account.utils import complete_signup
from dj_rest_auth.registration.views import RegisterView
from django.utils.translation import gettext_lazy as _

from users.serializers.auth import RegisterUserSerializer
from users.serializers.user import UserSerializer


class RegisterAPIView(RegisterView):
    """
    POST /api/auth/register/
    """
    serializer_class = RegisterUserSerializer
    token_model = None

    def get_response_data(self, user) -> dict:
        if allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY:
            return {'detail': _('Verification e-mail sent.')}

        return UserSerializer(user).data

    def perform_create(self, serializer: RegisterUserSerializer):
        # behaviour from dj_rest_auth but without creating drf token
        user = serializer.save(request=self.request)

        complete_signup(
            request=self.request._request,
            user=user,
            email_verification=allauth_settings.EMAIL_VERIFICATION,
            success_url=None,
        )
        return user

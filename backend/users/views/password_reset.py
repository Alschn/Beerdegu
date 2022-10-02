from dj_rest_auth.views import PasswordResetView

from users.serializers.auth import UserPasswordResetSerializer


class PasswordResetAPIView(PasswordResetView):
    """
    POST /api/auth/password/reset/
    """
    serializer_class = UserPasswordResetSerializer

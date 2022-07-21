from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterUserSerializer, UserPasswordResetSerializer


class RegisterAPIView(RegisterView):
    """
    POST /auth/register/
    """
    serializer_class = RegisterUserSerializer


class LoginAPIView(LoginView):
    """
    POST /auth/login/
    """
    pass


class LogoutAPIView(LogoutView):
    """
    POST /auth/logout/
    """
    permission_classes = [IsAuthenticated]


class PasswordChangeAPIView(PasswordChangeView):
    """
    POST /auth/password/change/
    """
    permission_classes = [IsAuthenticated]


class PasswordResetAPIView(PasswordResetView):
    """
    POST /auth/password/reset/
    """
    serializer_class = UserPasswordResetSerializer


class PasswordResetConfirmAPIView(PasswordResetConfirmView):
    """
    POST /auth/password/reset/confirm/
    """
    pass

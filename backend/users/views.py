from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView, PasswordChangeView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterUserSerializer


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

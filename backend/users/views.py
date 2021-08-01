from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView
from rest_framework.permissions import IsAuthenticated

from .serializers import RegisterUserSerializer


class RegisterAPIView(RegisterView):
    serializer_class = RegisterUserSerializer


class LoginAPIView(LoginView):
    pass


class LogoutAPIView(LogoutView):
    permission_classes = [IsAuthenticated]

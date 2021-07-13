from dj_rest_auth.registration.views import RegisterView
from dj_rest_auth.views import LoginView, LogoutView

from .serializers import RegisterUserSerializer


class RegisterAPIView(RegisterView):
    serializer_class = RegisterUserSerializer
    authentication_classes = []


class LoginAPIView(LoginView):
    authentication_classes = []


class LogoutAPIView(LogoutView):
    pass

from dj_rest_auth.views import LogoutView
from rest_framework.permissions import IsAuthenticated


class LogoutAPIView(LogoutView):
    """
    POST /auth/logout/
    """
    permission_classes = [IsAuthenticated]

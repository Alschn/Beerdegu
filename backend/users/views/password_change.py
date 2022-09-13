from dj_rest_auth.views import PasswordChangeView
from rest_framework.permissions import IsAuthenticated


class PasswordChangeAPIView(PasswordChangeView):
    """
    POST /auth/password/change/
    """
    permission_classes = [IsAuthenticated]

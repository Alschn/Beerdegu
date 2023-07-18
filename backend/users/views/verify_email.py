from dj_rest_auth.registration.views import VerifyEmailView


class VerifyEmailAPIView(VerifyEmailView):
    """
    POST /api/auth/register/confirm-email/
    """
    # disable authentication for this endpoint
    authentication_classes = []

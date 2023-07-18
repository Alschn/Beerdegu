from typing import Any

from dj_rest_auth.registration.views import VerifyEmailView
from django.views.decorators.csrf import csrf_exempt
from rest_framework.request import Request
from rest_framework.response import Response


class VerifyEmailAPIView(VerifyEmailView):
    """
    POST /api/auth/register/confirm-email/
    """

    @csrf_exempt
    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        return super().post(request, *args, **kwargs)

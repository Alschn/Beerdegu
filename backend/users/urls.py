from django.urls import path, re_path
from django.views.generic import TemplateView

from .views import (
    RegisterAPIView, LoginAPIView,
    LogoutAPIView, PasswordChangeAPIView,
    PasswordResetAPIView, PasswordResetConfirmAPIView,
    JWTObtainPairView, JWTRefreshView, JWTVerifyView
)

urlpatterns = [
    # jwt authentication
    path('auth/token/', JWTObtainPairView.as_view(), name='auth-jwt-login'),
    path('auth/token/refresh/', JWTRefreshView.as_view(), name='auth-jwt-refresh'),
    path('auth/token/verify/', JWTVerifyView.as_view(), name='auth-jwt-verify'),

    # token authentication
    path('auth/login/', LoginAPIView.as_view(), name='auth-login'),
    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),

    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/password/change/', PasswordChangeAPIView.as_view(), name='auth-password-change'),

    # password reset with email
    path('auth/password/reset/', PasswordResetAPIView.as_view(), name='auth-password-reset'),
    path(
        'auth/password/reset/confirm/<uidb64>/<token>/',
        PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'
    ),

    # This url is used by django-allauth and empty TemplateView is
    # defined just to allow reverse() call inside app, for example when email
    # with verification link is being sent, then it's required to render email
    # content.
    re_path(
        r'^auth/account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email',
    ),
]

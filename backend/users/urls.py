from django.urls import path

from .views import (
    RegisterAPIView, LogoutAPIView, PasswordChangeAPIView,
    PasswordResetAPIView, PasswordResetConfirmAPIView,
    JWTObtainPairView, JWTRefreshView, JWTVerifyView,
    GoogleLoginAPIView, GoogleAuthURLAPIView,
    VerifyEmailAPIView, ResendEmailAPIView
)

urlpatterns = [
    # jwt authentication
    path('auth/token/', JWTObtainPairView.as_view(), name='auth-jwt-login'),
    path('auth/token/refresh/', JWTRefreshView.as_view(), name='auth-jwt-refresh'),
    path('auth/token/verify/', JWTVerifyView.as_view(), name='auth-jwt-verify'),

    path('auth/logout/', LogoutAPIView.as_view(), name='auth-logout'),
    path('auth/register/', RegisterAPIView.as_view(), name='auth-register'),
    path('auth/password/change/', PasswordChangeAPIView.as_view(), name='auth-password-change'),

    # password reset with email
    path('auth/password/reset/', PasswordResetAPIView.as_view(), name='auth-password-reset'),
    path(
        'auth/password/reset/confirm/<str:uidb64>/<str:token>/',
        PasswordResetConfirmAPIView.as_view(), name='password_reset_confirm'
    ),

    # google auth url and login
    path('auth/providers/google/url/', GoogleAuthURLAPIView.as_view(), name='auth-google-login-url'),
    path('auth/providers/google/', GoogleLoginAPIView.as_view(), name='auth-google-login'),

    # email verification
    path(
        'auth/register/confirm-email/', VerifyEmailAPIView.as_view(),
        name='account_email_verification_sent',
    ),
    path(
        'auth/register/resend-email/', ResendEmailAPIView.as_view(),
        name='account_email_verification_resend',
    )
]

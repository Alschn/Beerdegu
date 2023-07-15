from allauth.account import app_settings as allauth_settings
from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenRefreshSerializer,
    TokenVerifySerializer,
    TokenObtainPairSerializer as BaseTokenObtainPairSerializer
)

from users.forms.password_reset import UserPasswordResetForm
from users.utils import (
    ACCESS_TOKEN_KEY,
    REFRESH_TOKEN_KEY
)


class RegisterUserSerializer(RegisterSerializer):
    password1 = serializers.CharField(
        label='Password',
        write_only=True,
        style={'input_type': 'password'}
    )
    password2 = serializers.CharField(
        label='Confirm Password',
        write_only=True,
        style={'input_type': 'password'}
    )


class UserPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return UserPasswordResetForm


class TokenObtainPairSerializer(BaseTokenObtainPairSerializer):

    def _validate_user_email_is_verified(self):
        is_email_verification_mandatory = (
            allauth_settings.EMAIL_VERIFICATION == allauth_settings.EmailVerificationMethod.MANDATORY
        )
        if not is_email_verification_mandatory:
            return

        user = self.user
        verified_emails = user.emailaddress_set.filter(email=user.email, verified=True)

        if not verified_emails.exists():
            raise serializers.ValidationError(_('E-mail is not verified.'))

    def validate(self, attrs: dict) -> dict:
        data = super().validate(attrs)

        self._validate_user_email_is_verified()

        refresh = self.get_token(self.user)

        data["refresh"] = str(refresh)
        data["access"] = str(refresh.access_token)
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
        token['email'] = user.email
        return token


class CookieTokenRefreshSerializer(TokenRefreshSerializer):

    def validate(self, attrs: dict):
        # If refresh token was found in cookies,
        # use it instead of the one from request body (request body can be empty)
        if refresh := self.context['request'].COOKIES.get(REFRESH_TOKEN_KEY):
            attrs['refresh'] = refresh

        return super().validate(attrs)


class CookieTokenVerifySerializer(TokenVerifySerializer):

    def validate(self, attrs: dict):
        # If access token was found in cookies,
        # use it instead of the one from request body (request body can be empty)
        if access := self.context['request'].COOKIES.get(ACCESS_TOKEN_KEY):
            attrs['token'] = access

        return super().validate(attrs)

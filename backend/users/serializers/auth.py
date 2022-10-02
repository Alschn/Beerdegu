from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
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
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['username'] = user.username
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

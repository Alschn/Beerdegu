from dj_rest_auth.registration.serializers import RegisterSerializer
from dj_rest_auth.serializers import PasswordResetSerializer
from django.contrib.auth.models import User
from rest_framework import serializers

from users.forms.password_reset import UserPasswordResetForm


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


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username']


class UserPasswordResetSerializer(PasswordResetSerializer):

    @property
    def password_reset_form_class(self):
        return UserPasswordResetForm

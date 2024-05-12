from allauth.account.models import EmailAddress
from django.contrib.auth import get_user_model
from django.contrib.sites.models import Site
from django.test import TestCase, override_settings
from drf_standardized_errors.openapi_serializers import ValidationErrorEnum, ClientErrorEnum
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APIClient

from core.shared.unit_tests import ExceptionResponse

User = get_user_model()

FRONTEND_SITE_NAME = 'localhost:8000'
FRONTEND_DOMAIN = f'http://{FRONTEND_SITE_NAME}'


@override_settings(FRONTEND_SITE_NAME=FRONTEND_SITE_NAME)
class AuthViewsTests(TestCase):
    register_url = reverse_lazy('auth-register')
    jwt_login_url = reverse_lazy('auth-jwt-login')
    logout_url = reverse_lazy('auth-logout')

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        user = User.objects.create_user(
            username='Test',
            email='test@example.com',
            password='abcdefg'
        )
        cls.user = user
        EmailAddress.objects.create(
            user=user,
            email=user.email,
        )
        Site.objects.create(
            domain=FRONTEND_DOMAIN,
            name=FRONTEND_SITE_NAME
        )

    def test_register_success(self):
        payload = {
            'username': 'Test2',
            'email': 'test2@example.com',
            'password1': 'verysecretpassword123',
            'password2': 'verysecretpassword123',
        }
        response = self.client.post(self.register_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('detail', response_json)

    def test_register_invalid_email(self):
        payload = {
            'username': 'Halo',
            'email': 'abc',
            'password1': '123ogpasd2',
            'password2': '123ogpasd2',
        }
        response = self.client.post(self.register_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('email')
        self.assertEqual(err.code, 'invalid')
        self.assertEqual(err.detail, 'Enter a valid email address.')

    def test_register_passwords_not_matching(self):
        payload = {
            'username': 'Halo',
            'email': 'abc@gmail.com',
            'password1': '123ogpasd2',
            'password2': '123ogpasd1',
        }
        response = self.client.post(self.register_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('non_field_errors')
        self.assertEqual(err.detail, "The two password fields didn't match.")

    def test_register_user_already_exists(self):
        payload = {
            'username': 'Test',
            'email': 'test@gmail.com',
            'password1': '!@#sdafggdf',
            'password2': '!@#sdafggdf',
        }
        response = self.client.post(self.register_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        error_attrs = res.attrs
        self.assertIn('username', error_attrs)

    def test_login_success(self):
        username = 'Test1'
        password = 'abcdefg'
        user = User.objects.create_user(
            username=username,
            email='test1@example.com',
            password=password
        )
        EmailAddress.objects.create(
            user=user,
            email=user.email,
            verified=True,
        )

        payload = {
            'username': username,
            'password': password,
        }
        response = self.client.post(self.jwt_login_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response_json)
        self.assertIn('refresh', response_json)

    def test_login_email_unverified(self):
        username = 'Test1'
        password = 'abcdefg'
        User.objects.create_user(
            username=username,
            email='test1@example.com',
            password=password
        )
        payload = {
            'username': 'Test',
            'password': 'abcdefg',
        }
        response = self.client.post(self.jwt_login_url, payload)

        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('email')
        self.assertEqual(err.code, 'email_not_verified')
        self.assertEqual(err.detail, 'E-mail is not verified.')

    def test_login_invalid_data(self):
        payload = {
            'username': 'Test',
            'password': 'xd',
        }
        response = self.client.post(self.jwt_login_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        err = res.get_error_by_code('no_active_account')
        self.assertEqual(err.detail, 'No active account found with the given credentials')

    def test_logout(self):
        self.client.login(username='Test', password='abcdefg')
        self.client.force_authenticate(self.user)
        response = self.client.post(self.logout_url, {})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, {'message': 'Successfully logged out.'})

    def test_logout_unauthorized(self):
        response = self.client.post(self.logout_url, {})
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        err = res.get_error_by_code('not_authenticated')
        self.assertEqual(err.detail, 'Authentication credentials were not provided.')

    def test_verify_email(self):
        pass

    def test_verify_email_invalid_key(self):
        pass

    def test_verify_email_already_verified(self):
        pass

    def test_resend_email(self):
        pass

    def test_resend_email_already_verified(self):
        pass

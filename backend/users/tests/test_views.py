from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from users.serializers.user import UserSerializer


class AuthViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='Test',
            password='abcdefg'
        )

    def test_register_success(self):
        response = self.client.post(reverse('auth-register'), {
            'username': 'Test2',
            'email': 'test2@gmail.com',
            'password1': 'verysecretpassword123',
            'password2': 'verysecretpassword123',
        })
        user = User.objects.get(username='Test2')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.json(), UserSerializer(user).data)

    def test_register_invalid_email(self):
        response = self.client.post(reverse('auth-register'), {
            'username': 'Halo',
            'email': 'abc',
            'password1': '123ogpasd2',
            'password2': '123ogpasd2',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'email': ['Enter a valid email address.']})

    def test_register_passwords_not_matching(self):
        response2 = self.client.post(reverse('auth-register'), {
            'username': 'Halo',
            'email': 'abc@gmail.com',
            'password1': '123ogpasd2',
            'password2': '123ogpasd1',
        })
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response2.json(), {'non_field_errors': ["The two password fields didn't match."]})

    def test_register_user_already_exists(self):
        response = self.client.post(reverse('auth-register'), {
            'username': 'Test',
            'email': 'test@gmail.com',
            'password1': '!@#sdafggdf',
            'password2': '!@#sdafggdf',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'username': ['A user with that username already exists.']})

    def test_login_success(self):
        response = self.client.post(reverse('auth-jwt-login'), {
            'username': 'Test',
            'password': 'abcdefg',
        })
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue('access' in response_json)
        self.assertTrue('refresh' in response_json)

    def test_login_invalid_data(self):
        response = self.client.post(reverse('auth-jwt-login'), {
            'username': 'Test',
            'password': 'xd',
        })
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'No active account found with the given credentials'})

    def test_logout(self):
        self.client.login(username='Test', password='abcdefg')
        self.client.force_authenticate(self.user)
        response = self.client.post(reverse('auth-logout'), {})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Successfully logged out.'})

    def test_logout_unauthorized(self):
        response = self.client.post(reverse('auth-logout'), {})
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertEqual(response.json(), {'detail': 'Authentication credentials were not provided.'})

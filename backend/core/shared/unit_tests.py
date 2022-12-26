from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework.test import APIClient

User = get_user_model()


class APITestCase(TestCase):
    USER_NAME = 'Test'
    USER_PASSWORD = '!@#$%'

    def setUp(self):
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls):
        cls.user = User.objects.create_user(
            username=cls.USER_NAME,
            password=cls.USER_PASSWORD
        )

    def _require_login_and_auth(self, user: User = None, username: str = None, password: str = None):
        if not user:
            username = self.USER_NAME
            password = self.USER_PASSWORD
            user = self.user
        else:
            user = User.objects.get(username=username)

        self.client.login(username=username, password=password)
        self.client.force_authenticate(user)

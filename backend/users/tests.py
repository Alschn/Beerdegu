from django.test import TestCase
from rest_framework.test import APIClient


class AuthViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        pass

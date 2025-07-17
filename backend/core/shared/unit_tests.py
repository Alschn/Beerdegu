import dataclasses
import typing

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


class ResponseLikeProtocol(typing.Protocol):
    status_code: int

    def json(self) -> dict:
        ...


@dataclasses.dataclass
class ExceptionDict:
    code: str
    detail: str
    attr: str = None


@dataclasses.dataclass
class ExceptionResponse:
    """
    Dataclass for easier handling of exception responses from the API in unit tests.
    """

    # Content extracted from response JSON.
    type: str
    errors: list[ExceptionDict]

    # Optional response object for additional information.
    _response: ResponseLikeProtocol = None

    @classmethod
    def from_dict(cls, data: dict) -> 'ExceptionResponse':
        errors = [ExceptionDict(**error) for error in data['errors']]
        return cls(
            type=data['type'],
            errors=errors,
        )

    @classmethod
    def from_response(cls, response: ResponseLikeProtocol) -> 'ExceptionResponse':
        obj = cls.from_dict(response.json())
        obj._response = response
        return obj

    @property
    def status(self) -> int | None:
        return self._response.status_code if self._response else None

    @property
    def status_code(self) -> int | None:
        return self.status

    @property
    def codes(self) -> list[str]:
        return [error.code for error in self.errors]

    @property
    def details(self) -> list[str]:
        return [error.detail for error in self.errors]

    @property
    def attrs(self) -> list[str]:
        return [error.attr for error in self.errors]

    def get_error_by_code(self, code: typing.Any) -> ExceptionDict:
        for error in self.errors:
            if error.code == str(code):
                return error

        raise ValueError(f'Code "{code}" not found in errors.')

    def get_error_by_attr(self, attr: str) -> ExceptionDict:
        for error in self.errors:
            if error.attr == attr:
                return error

        raise ValueError(f'Attribute "{attr}" not found in errors.')

    def contains_error_code(self, code: typing.Any) -> bool:
        try:
            self.get_error_by_code(code)
            return True
        except ValueError:
            return False

    def contains_error_attr(self, attr: str) -> bool:
        try:
            self.get_error_by_attr(attr)
            return True
        except ValueError:
            return False

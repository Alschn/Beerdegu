from django.contrib.auth.models import User
from django.test import TestCase

from rooms.models import Room


class RoomTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='Test',
            password='!@#$%'
        )

    def test_create_room(self):
        """Checks if room was created and host was added to users."""
        room = Room.objects.create(
            name='ABCDEFGH',
            host=self.user,
            slots=4,
        )
        self.assertEqual(Room.objects.get(name='ABCDEFGH'), room)
        self.assertIn(self.user, room.users.all())


class RoomsAPIViewsTest(TestCase):
    pass

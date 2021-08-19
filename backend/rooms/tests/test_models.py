from django.contrib.auth.models import User
from django.test import TestCase

from rooms.models import Room


class RoomsModelsTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='Test',
            password='!@#$%'
        )
        cls.room1 = Room.objects.create(
            name='TestRoom',
            host=cls.user,
            slots=4,
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

    def test_room_to_string(self):
        self.assertEqual(str(self.room1), "'TestRoom' 1/4 - waiting")

    def test_rating_to_string(self):
        pass

    def test_beer_in_room_to_string(self):
        pass

    def test_user_in_room_to_string(self):
        pass

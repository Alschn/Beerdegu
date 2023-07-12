from django.contrib.auth import get_user_model
from django.test import TestCase

from beers.models import Beer
from rooms.models import Room, Rating, UserInRoom, BeerInRoom

User = get_user_model()


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
        rating = Rating.objects.create(added_by=self.user, note=10)
        self.assertEqual(str(rating), f'10 by {self.user.username}')

    def test_rating_without_note_to_string(self):
        rating = Rating.objects.create(added_by=self.user)
        self.assertEqual(str(rating), f'None by {self.user.username}')

    def test_beer_in_room_to_string(self):
        user = User.objects.create_user(username="test2", password="test2")
        beer = Beer.objects.create(name="Atak Chmielu", percentage="6.1", volume_ml=500)
        room = Room.objects.create(name="testroom", slots=4, host=user, state=Room.State.STARTING)
        beer_in_room = BeerInRoom.objects.create(beer=beer, room=room)
        self.assertEqual(str(beer_in_room), f'{room.name} - #{beer_in_room.order} - {beer}')

    def test_user_in_room_to_string(self):
        user = User.objects.create_user(username="test3", password="test3")
        room = Room.objects.create(name="testr00m", slots=3, host=user, state=Room.State.STARTING)
        user_in_room = UserInRoom.objects.create(user=user, room=room)
        self.assertEqual(str(user_in_room), f'{user.username} - {room.name}')

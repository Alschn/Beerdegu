from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from django.test import TestCase

from rooms.async_db import get_users_in_room
from rooms.models import Room
from users.serializers import UserSerializer


# django.db.utils.InterfaceError: connection already closed
# when running postgres on github actions
# locally tests run fine


class RoomsAsyncDbTests(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(username='Test1', password='!@#$%')
        cls.room = Room.objects.create(name='12345678', host=cls.user, slots=3)
        cls.user2 = User.objects.create_user(username='Test2', password='!@#$%')
        cls.user3 = User.objects.create_user(username='Test3', password='!@#$%')
        cls.room.users.add(*[cls.user2, cls.user3])

    async def test_get_users_in_room(self):
        # users = await get_users_in_room(room_name='12345678')
        # self.assertEqual(users, UserSerializer(users, many=True).data)
        pass

    async def test_bump_users_last_active_field(self):
        pass  # to do

    async def test_save_user_form(self):
        pass  # to do

    async def test_get_user_form_data(self):
        pass  # to do

    async def test_get_beers_in_room(self):
        pass  # to do

    async def get_current_room(self):
        pass  # to do

    async def change_room_state_to(self):
        pass  # to do

    async def get_final_user_beer_ratings(self):
        pass  # to do

    async def get_final_beers_ratings(self):
        pass  # to do

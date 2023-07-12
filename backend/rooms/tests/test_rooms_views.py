import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from beers.models import Beer
from beers.serializers import BeerSerializer
from rooms.models import Room
from rooms.serializers import RoomSerializer, DetailedRoomSerializer
from rooms.serializers.room import RoomListSerializer

User = get_user_model()


class RoomsAPIViewsTests(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = User.objects.create_user(username='Test', password='!@#$%')
        cls.user2 = User.objects.create_user(username='Test2', password='!@#$%')
        cls.user3 = User.objects.create_user(username='Test3', password='abcdef123@')
        cls.room = Room.objects.create(name='12345678', host=cls.user1, slots=4)
        cls.room_with_pass = Room.objects.create(
            name='abcdefgh', password='password', slots=2,
            host=cls.user3
        )
        cls.room_with_pass.beers.add(*Beer.objects.bulk_create([
            Beer(id=50, name='Atak Chmielu', percentage=6.1, volume_ml=500),
            Beer(id=51, name='Maniac', percentage=8, volume_ml=500),
            Beer(id=52, name='Triple NEIPA', percentage=9.2, volume_ml=500),
            Beer(id=53, name='Diablo Verde', percentage=7.6, volume_ml=500),
        ]))

    # noinspection PyUnresolvedReferences
    def _require_login_and_auth(self, user: User) -> None:
        self.client.login(username=user.username, password=user.password)
        self.client.force_authenticate(user)

    def test_user_is_in_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/xd/in/')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'detail': 'Not found.'}, to_json)

    def test_user_is_not_in_room(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.get('/api/rooms/12345678/in/')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual({'message': 'User is not part of this room!'}, to_json)

    def test_user_is_in_room_and_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/12345678/in/')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', to_json)
        self.assertIn('token', to_json)
        self.assertEqual(to_json['is_host'], True)

    def test_user_is_in_room_not_host(self):
        self._require_login_and_auth(user=self.user2)
        self.room.users.add(self.user2)
        response = self.client.get('/api/rooms/12345678/in/')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', to_json)
        self.assertIn('token', to_json)
        self.assertEqual(to_json['is_host'], False)

    def test_join_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/aha/join/', data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_join_room_already_in(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/12345678/join/', data={'password': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_join_room_full(self):
        room = Room.objects.create(
            name='FULL',
            slots=1,
            host=self.user2
        )
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(room.slots, room.users.count())
        response = self.client.put('/api/rooms/FULL/join/', data={'password': ''})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('slots', response.json())

    def test_join_room_success(self):
        self._require_login_and_auth(user=self.user2)
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/12345678/join/', data={'password': ''})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user2, r.users.all())

    def test_join_room_with_password_not_in_body(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/abcdefgh/join/', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('password', response.json())
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_password_invalid(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/abcdefgh/join/', data={'password': '12345'})
        self.assertIn('password', response.json())
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_with_password_success(self):
        self._require_login_and_auth(user=self.user1)
        r = Room.objects.get(name='abcdefgh')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/abcdefgh/join/', data={'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user1, r.users.all())

    def test_leave_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete('/api/rooms/aha/leave/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'detail': 'Not found.'})

    def test_leave_room_not_in(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.delete('/api/rooms/12345678/leave/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': f'Test2 is not inside this room!'})

    def test_leave_room_success(self):
        self._require_login_and_auth(user=self.user1)
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.delete('/api/rooms/12345678/leave/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Test has left room 12345678!'})
        self.assertEqual(r.users.count(), 0)
        self.assertNotIn(self.user1, r.users.all())

    def test_list_rooms(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['results'],
            second=RoomListSerializer(Room.objects.order_by('id'), many=True).data
        )

    def test_create_room(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.post('/api/rooms/', data={
            'name': 'Good',
            'password': 'anything',
            'slots': 5,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Room.objects.filter(name='Good').exists())

    def test_create_room_name_not_unique(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.post('/api/rooms/', data={
            'name': '12345678',
            'password': '',
            'slots': 3,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'name': ['room with this name already exists.']})

    def test_create_room_wrong_slots_number(self):
        self._require_login_and_auth(user=self.user2)
        r1 = self.client.post('/api/rooms/', data={
            'name': 'ooo', 'password': 'anything', 'slots': 11,
        })
        self.assertEqual(r1.status_code, status.HTTP_400_BAD_REQUEST)

        r2 = self.client.post('/api/rooms/', data={
            'name': 'ooo', 'password': 'anything', 'slots': -1,
        })
        self.assertEqual(r2.status_code, status.HTTP_400_BAD_REQUEST)

        r3 = self.client.post('/api/rooms/', data={
            'name': 'ooo', 'password': 'anything', 'slots': 5.6,
        })
        self.assertEqual(r3.status_code, status.HTTP_400_BAD_REQUEST)

        r4 = self.client.post('/api/rooms/', data={
            'name': 'ooo', 'password': 'anything', 'slots': 'a',
        })
        self.assertEqual(r4.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_room_but_user_already_host_in_other_room(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.post('/api/rooms/', data={
            'name': 'Blahblah',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('host', response.json())

    def test_get_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(f'/api/rooms/{self.room.name}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), DetailedRoomSerializer(self.room).data)

    @unittest.skip('Currently disabled')
    def test_update_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        lookup = self.room.name
        self.assertEqual(self.room.state, 'WAITING')
        response = self.client.patch(f'/api/rooms/{lookup}/', {
            'state': 'IN_PROGRESS'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.state, 'IN_PROGRESS')
        self.assertEqual(
            first=response.json(),
            second=RoomSerializer(Room.objects.get(name=lookup)).data
        )

    @unittest.skip('Currently disabled')
    def test_update_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(self.room.state, 'WAITING')
        response = self.client.patch(f'/api/rooms/{self.room_with_pass.name}/', {
            'state': 'IN_PROGRESS'
        })
        self.assertEqual(self.room.state, 'WAITING')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @unittest.skip('Currently disabled')
    def test_delete_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(f'/api/rooms/{self.room.name}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @unittest.skip('Currently disabled')
    def test_delete_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(f'/api/rooms/{self.room_with_pass.name}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_update_delete_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response_get = self.client.get('/api/rooms/123/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # self._require_login_and_auth(user=self.user1)
        # response_put = self.client.put('/api/rooms/123/', {})
        # self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_patch = self.client.patch('/api/rooms/123/', {})
        # self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_delete = self.client.delete('/api/rooms/123/')
        # self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_beers_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.get('/api/rooms/abcdefgh/beers/')
        queryset = Beer.objects.filter(room__name='abcdefgh').order_by('id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            BeerSerializer(queryset, many=True).data
        )

    def test_list_beers_in_room_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        response = self.client.get('/api/rooms/abcdefgh/beers/')
        queryset = Beer.objects.filter(room__name='abcdefgh').order_by('id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            BeerSerializer(queryset, many=True).data
        )

    def test_list_beers_in_room_which_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.get('/api/rooms/xdddddd/beers/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_beer_no_id_in_request(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer_id', response.json())

    def test_add_beer_which_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers/', {
            'beer_id': 10000,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer_id', response.json())

    def test_add_beer_room_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/XDDDD/beers/', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_add_beer_already_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers/', {
            'beer_id': 50,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer_id', response.json())

    def test_add_beer_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        beer = Beer.objects.create(name='user_not_host', percentage=5, volume_ml=500)
        response = self.client.put('/api/rooms/abcdefgh/beers/', {
            'beer_id': beer.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_add_beer_success(self):
        self._require_login_and_auth(self.user3)
        room_name = 'abcdefgh'
        beer_to_add = Beer.objects.create(name='test', percentage=5, volume_ml=500)
        beers_before = Beer.objects.filter(room__name=room_name).order_by('id')
        self.assertEqual(beers_before.count(), 4)
        response = self.client.put(f'/api/rooms/{room_name}/beers/', {
            'beer_id': beer_to_add.id
        })
        beers_after = Beer.objects.filter(room__name=room_name).order_by('beerinroom__order')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            BeerSerializer(beers_after, many=True).data
        )
        self.assertEqual(beers_after.count(), 5)

    def test_delete_no_id_in_url_parameters(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers/')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_beer_room_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/XDDDD/beers/')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_beer_not_found_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers/?id=100')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer_id', response.json())

    def test_delete_beer_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        response = self.client.delete('/api/rooms/abcdefgh/beers/?id=50')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_beer_success(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers/?beer_id=53')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

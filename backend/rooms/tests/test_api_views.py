from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

from beers.models import Beer
from beers.serializers import BeerSerializer
from rooms.models import Room
from rooms.serializers import RoomSerializer, DetailedRoomSerializer


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
            Beer(id=10, name='Atak Chmielu', percentage=6.1, volume_ml=500),
            Beer(id=11, name='Maniac', percentage=8, volume_ml=500),
            Beer(id=12, name='Triple NEIPA', percentage=9.2, volume_ml=500),
            Beer(id=13, name='Diablo Verde', percentage=7.6, volume_ml=500),
        ]))

    # noinspection PyUnresolvedReferences
    def _require_login_and_auth(self, user: User) -> None:
        self.client.login(username=user.username, password=user.password)
        self.client.force_authenticate(user)

    def test_user_is_in_room_no_code_given(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/in')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'message': 'Missing code parameter in query!'}, to_json)

    def test_user_is_in_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/in?code=xd')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'message': 'Room with given code not found!'}, to_json)

    def test_user_is_not_in_room(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual({'message': 'User is not part of this room!'}, to_json)

    def test_user_is_in_room_and_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {'message': 'Test is in this room.', 'is_host': True},
            to_json
        )

    def test_user_is_in_room_not_host(self):
        self._require_login_and_auth(user=self.user2)
        self.room.users.add(self.user2)
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {'message': 'Test2 is in this room.', 'is_host': False},
            to_json
        )

    def test_join_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/aha/join', data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room not found!'})

    def test_join_room_already_in(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/12345678/join', data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'User is already in this room!'})

    def test_join_room_full(self):
        room = Room.objects.create(
            name='FULL',
            slots=1,
            host=self.user2
        )
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(room.slots, room.users.count())
        response = self.client.put('/api/rooms/FULL/join', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'message': f'Room FULL is full!'})

    def test_join_room_success(self):
        self._require_login_and_auth(user=self.user2)
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/12345678/join', data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Joined room 12345678'})
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user2, r.users.all())

    def test_join_room_with_password_not_in_body(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/abcdefgh/join', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Room abcdefgh is protected. No password found in body'})
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_password_invalid(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put('/api/rooms/abcdefgh/join', data={'password': '12345'})
        self.assertEqual(response.json(), {'message': 'Invalid password!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_with_password_success(self):
        self._require_login_and_auth(user=self.user1)
        r = Room.objects.get(name='abcdefgh')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/abcdefgh/join', data={'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Joined room abcdefgh'})
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user1, r.users.all())

    def test_leave_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete('/api/rooms/aha/leave')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room not found!'})

    def test_leave_room_not_in(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.delete('/api/rooms/12345678/leave')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': f'Test2 is not inside this room!'})

    def test_leave_room_success(self):
        self._require_login_and_auth(user=self.user1)
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.delete('/api/rooms/12345678/leave')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Test has left room 12345678!'})
        self.assertEqual(r.users.count(), 0)
        self.assertNotIn(self.user1, r.users.all())

    def test_list_rooms(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get('/api/rooms/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=DetailedRoomSerializer(Room.objects.all(), many=True).data
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
        response = self.client.post('/api/rooms/', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.json(),
            {'message': 'User is already a host of another room. Leave it and try again!'}
        )

    def test_get_room_by_id(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(f'/api/rooms/{self.room.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), DetailedRoomSerializer(self.room).data)

    def test_update_room_by_id(self):
        self._require_login_and_auth(user=self.user1)
        lookup_id = self.room.id
        self.assertEqual(self.room.state, 'WAITING')
        response = self.client.patch(f'/api/rooms/{lookup_id}/', {
            'state': 'IN_PROGRESS'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.room.refresh_from_db()
        self.assertEqual(self.room.state, 'IN_PROGRESS')
        self.assertEqual(
            first=response.json(),
            second=RoomSerializer(Room.objects.get(id=lookup_id)).data
        )

    def test_update_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(self.room.state, 'WAITING')
        response = self.client.patch(f'/api/rooms/{self.room_with_pass.id}/', {
            'state': 'IN_PROGRESS'
        })
        self.assertEqual(self.room.state, 'WAITING')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {'detail': 'You do not have permission to perform this action.'}
        )

    def test_delete_room_by_id(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(f'/api/rooms/{self.room.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(f'/api/rooms/{self.room_with_pass.id}/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(
            response.json(),
            {'detail': 'You do not have permission to perform this action.'}
        )

    def test_get_update_delete_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response_get = self.client.get('/api/rooms/123/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        self._require_login_and_auth(user=self.user1)
        response_put = self.client.put('/api/rooms/123/', {})
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        response_patch = self.client.patch('/api/rooms/123/', {})
        self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.client.delete('/api/rooms/123/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_list_beers_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.get('/api/rooms/abcdefgh/beers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'room': 'abcdefgh',
                'beers': BeerSerializer(Beer.objects.filter(room__name='abcdefgh'), many=True).data
            }
        )

    def test_list_beers_in_room_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        response = self.client.get('/api/rooms/abcdefgh/beers')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            {
                'room': 'abcdefgh',
                'beers': BeerSerializer(Beer.objects.filter(room__name='abcdefgh'), many=True).data
            }
        )

    def test_list_beers_in_room_which_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.get('/api/rooms/xdddddd/beers')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room with given name does not exist!'})

    def test_add_beer_no_id_in_request(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Beer id not found in request body!'})

    def test_add_beer_which_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers', {
            'beer_id': 10000,
        })
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Beer with given id does not exist!'})

    def test_add_beer_room_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/XDDDD/beers', {})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room with given name does not exist!'})

    def test_add_beer_already_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.put('/api/rooms/abcdefgh/beers', {
            'beer_id': 10,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Beer with given is already in this room!'})

    def test_add_beer_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        beer = Beer.objects.create(name='user_not_host', percentage=5, volume_ml=500)
        response = self.client.put('/api/rooms/abcdefgh/beers', {
            'beer_id': beer.id
        })
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_add_beer_success(self):
        self._require_login_and_auth(self.user3)
        beer_to_add = Beer.objects.create(name='test', percentage=5, volume_ml=500)
        beers_before = Beer.objects.filter(room__name='abcdefgh')
        self.assertEqual(beers_before.count(), 4)
        response = self.client.put('/api/rooms/abcdefgh/beers', {
            'beer_id': beer_to_add.id
        })
        beers_after = Beer.objects.filter(room__name='abcdefgh')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            {
                'room': 'abcdefgh',
                'beers': BeerSerializer(beers_after, many=True).data
            }
        )
        self.assertEqual(beers_after.count(), 5)

    def test_delete_no_id_in_url_parameters(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Beer id not found in request parameters!'})

    def test_delete_beer_room_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/XDDDD/beers')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room with given name does not exist!'})

    def test_delete_beer_not_found_in_room(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers?id=100')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Beer with given id was not found in this room!'})

    def test_delete_beer_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        response = self.client.delete('/api/rooms/abcdefgh/beers?id=10')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'detail': 'You do not have permission to perform this action.'})

    def test_delete_beer_success(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete('/api/rooms/abcdefgh/beers?id=13')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': 'Successfully removed beer from room!'})

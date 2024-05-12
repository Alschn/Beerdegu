import unittest

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse_lazy
from drf_standardized_errors.openapi_serializers import (
    ClientErrorEnum,
    ErrorCode403Enum, ErrorCode404Enum, ValidationErrorEnum,
)
from rest_framework import status
from rest_framework.test import APIClient

from beers.models import Beer
from beers.serializers import BeerSerializer
from core.shared.factories import UserFactory, RoomFactory, BeerFactory
from core.shared.unit_tests import ExceptionResponse
from rooms.models import Room
from rooms.serializers import RoomSerializer, RoomDetailedSerializer
from rooms.serializers.room import RoomListSerializer, RESTRICTED_ROOM_NAMES

User = get_user_model()


class RoomsAPIViewsTests(TestCase):
    list_url = reverse_lazy('rooms-list')

    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = UserFactory(username='Test', password='!@#$%')
        cls.user2 = UserFactory(username='Test2', password='!@#$%')
        cls.user3 = UserFactory(username='Test3', password='abcdef123@')
        cls.room = RoomFactory(name='12345678', host=cls.user1, slots=4)
        cls.room_with_pass = RoomFactory(
            name='abcdefgh', password='password', slots=2,
            host=cls.user3
        )
        beers = Beer.objects.bulk_create([
            Beer(id=50, name='Atak Chmielu', percentage=6.1, volume_ml=500),
            Beer(id=51, name='Maniac', percentage=8, volume_ml=500),
            Beer(id=52, name='Triple NEIPA', percentage=9.2, volume_ml=500),
            Beer(id=53, name='Diablo Verde', percentage=7.6, volume_ml=500),
        ])
        cls.room_with_pass.beers.add(*beers)

    # noinspection PyUnresolvedReferences
    def _require_login_and_auth(self, user: User) -> None:
        self.client.login(username=user.username, password=user.password)
        self.client.force_authenticate(user)

    def test_user_is_in_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(
            reverse_lazy('rooms-user-in', args=('xd',))
        )

        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_user_is_not_in_room(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.get(
            reverse_lazy('rooms-user-in', args=('12345678',))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn('user_not_in_room', res.codes)

    def test_user_is_in_room_and_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(
            reverse_lazy('rooms-user-in', args=('12345678',))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response_json)
        self.assertIn('token', response_json)
        self.assertEqual(response_json['is_host'], True)

    def test_user_is_in_room_not_host(self):
        self._require_login_and_auth(user=self.user2)
        self.room.users.add(self.user2)
        response = self.client.get(
            reverse_lazy('rooms-user-in', args=('12345678',))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('message', response_json)
        self.assertIn('token', response_json)
        self.assertEqual(response_json['is_host'], False)

    def test_join_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=('aha',)),
            data={}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_join_room_already_in(self):
        self._require_login_and_auth(user=self.user1)
        room_name = '12345678'
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=(room_name,)),
            data={'password': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_join_room_full(self):
        room = RoomFactory(
            name='FULL',
            slots=1,
            host=self.user2
        )
        self.assertEqual(room.slots, room.users.count())

        self._require_login_and_auth(user=self.user1)
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=(room.name,)),
            data={'password': ''}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('slots')
        self.assertEqual(err.code, 'room_already_full')

    def test_join_room_success(self):
        room = Room.objects.get(name='12345678')
        self.assertEqual(room.users.count(), 1)

        self._require_login_and_auth(user=self.user2)
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=('12345678',)),
            data={'password': ''}
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(room.users.count(), 2)
        self.assertTrue(room.users.contains(self.user2))

    def test_join_room_with_password_not_in_body(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=('abcdefgh',)),
            data={}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('password')
        self.assertEqual(err.code, 'required')
        self.assertFalse(
            self.room_with_pass.users.contains(self.user1)
        )

    def test_join_room_password_invalid(self):
        self._require_login_and_auth(user=self.user1)
        payload = {'password': '12345'}
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=('abcdefgh',)),
            data=payload
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('password', res.attrs)

    def test_join_room_with_password_success(self):
        room = Room.objects.get(name='abcdefgh')
        self.assertEqual(room.users.count(), 1)

        self._require_login_and_auth(user=self.user1)
        payload = {'password': 'password'}
        response = self.client.put(
            reverse_lazy('rooms-user-join', args=('abcdefgh',)),
            data=payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(room.users.count(), 2)
        self.assertTrue(room.users.contains(self.user1))

    def test_leave_room_not_found(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(
            reverse_lazy('rooms-user-leave', args=('aha',))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_leave_room_not_in(self):
        self._require_login_and_auth(user=self.user2)
        response = self.client.delete(
            reverse_lazy('rooms-user-leave', args=('12345678',))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('user_not_in_room', res.codes)

    def test_leave_room_success(self):
        room = Room.objects.get(name='12345678')
        self.assertEqual(room.users.count(), 1)

        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(
            reverse_lazy('rooms-user-leave', args=(room.name,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, {'message': f'Test has left room {room.name}!'})
        self.assertEqual(room.users.count(), 0)
        self.assertFalse(room.users.contains(self.user1))

    def test_list_rooms(self):
        queryset = Room.objects.order_by('id')

        self._require_login_and_auth(user=self.user1)
        response = self.client.get(self.list_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json['results'],
            RoomListSerializer(queryset, many=True).data
        )

    def test_create_room(self):
        self._require_login_and_auth(user=self.user2)
        payload = {
            'name': 'Good',
            'password': 'anything',
            'slots': 5,
        }
        response = self.client.post(self.list_url, payload)
        queryset = Room.objects.filter(name='good')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(queryset.exists())

    def test_create_room_not_lowercase(self):
        self._require_login_and_auth(user=self.user2)
        payload = {
            'name': 'qWeRtY',
            'password': 'anything',
            'slots': 5,
        }
        response = self.client.post(self.list_url, payload)
        queryset = Room.objects.filter(name='qwerty')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(queryset.exists())

    def test_create_room_name_not_unique(self):
        self._require_login_and_auth(user=self.user2)
        payload = {
            'name': '12345678',
            'password': 'anything',
            'slots': 3,
        }
        response = self.client.post(self.list_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('name')
        self.assertEqual(err.code, 'unique')

    def test_create_room_name_restricted(self):
        restricted_names = RESTRICTED_ROOM_NAMES
        payload = {
            'password': 'anything',
            'slots': 3,
        }
        self._require_login_and_auth(user=self.user2)
        for name in restricted_names:
            data = {**payload, 'name': name}
            response = self.client.post(self.list_url, data=data)
            res = ExceptionResponse.from_response(response)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
            err = res.get_error_by_attr('name')
            self.assertEqual(err.code, 'room_name_restricted')

    def test_create_room_wrong_slots_number(self):
        self._require_login_and_auth(user=self.user2)
        payload = {
            'name': 'ooo', 'password': 'anything',
        }
        invalid_slots = (11, -1, 5.6, 'a')
        for slots in invalid_slots:
            data = {**payload, 'slots': slots}
            response = self.client.post(self.list_url, data=data)
            res = ExceptionResponse.from_response(response)
            self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
            self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
            self.assertIn('slots', res.attrs)

    def test_create_room_but_user_already_host_in_other_room(self):
        user = UserFactory(username='new_host_user')
        RoomFactory(name='test', host=user, state=Room.State.IN_PROGRESS)

        self._require_login_and_auth(user=user)

        response = self.client.post(
            self.list_url, data={'name': 'Blahblah'}
        )

        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('host')
        self.assertEqual(err.code, 'room_host_already_hosting')

    def test_get_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(
            reverse_lazy('rooms-detail', args=(self.room.name,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            RoomDetailedSerializer(self.room).data
        )

    @unittest.skip('Currently disabled')
    def test_update_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(self.room.state, Room.State.WAITING)

        room_name = self.room.name
        payload = {'state': str(Room.State.IN_PROGRESS)}

        response = self.client.patch(
            reverse_lazy('rooms-detail', args=(room_name,)),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.room.refresh_from_db()
        self.assertEqual(self.room.state, Room.State.IN_PROGRESS)
        self.assertEqual(
            response.json(),
            RoomSerializer(self.room).data
        )

    @unittest.skip('Currently disabled')
    def test_update_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        self.assertEqual(self.room.state, Room.State.WAITING)
        payload = {'state': str(Room.State.IN_PROGRESS)}
        response = self.client.patch(
            reverse_lazy('rooms-detail', args=(self.room_with_pass.name,)),
            payload
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode403Enum.PERMISSION_DENIED, res.codes)
        self.assertEqual(self.room.state, Room.State.WAITING)

    @unittest.skip('Currently disabled')
    def test_delete_room_by_name(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(
            reverse_lazy('rooms-detail', args=(self.room.name,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    @unittest.skip('Currently disabled')
    def test_delete_room_not_host(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.delete(
            reverse_lazy('rooms-detail', args=(self.room_with_pass.name,))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode403Enum.PERMISSION_DENIED, res.codes)

    def test_get_update_delete_room_doesnt_exist(self):
        self._require_login_and_auth(user=self.user1)
        response = self.client.get(
            reverse_lazy('rooms-detail', args=('123',))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_list_beers_in_room(self):
        room_name = 'abcdefgh'

        self._require_login_and_auth(self.user3)
        response = self.client.get(
            reverse_lazy('rooms-detail-beers', args=(room_name,))
        )
        response_json = response.json()
        queryset = Beer.objects.filter(rooms__name=room_name).order_by('id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            BeerSerializer(queryset, many=True).data
        )

    def test_list_beers_in_room_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)
        room_name = 'abcdefgh'
        response = self.client.get(
            reverse_lazy('rooms-detail-beers', args=(room_name,))
        )
        response = self.client.get(
            reverse_lazy('rooms-detail-beers', args=(room_name,))
        )
        queryset = Beer.objects.filter(rooms__name=room_name).order_by('id')
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
        room_name = 'abcdefgh'
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=(room_name,)),
            data={}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('beer_id', res.attrs)

    def test_add_beer_which_doesnt_exist(self):
        room_name = 'abcdefgh'
        beer_id = 10000

        self._require_login_and_auth(self.user3)
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=(room_name,)),
            data={'beer_id': beer_id}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('beer_id', res.attrs)

    def test_add_beer_room_doesnt_exist(self):
        room_name = 'XDDDD'

        self._require_login_and_auth(self.user3)
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=(room_name,)),
            data={}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_add_beer_already_in_room(self):
        room_name = 'abcdefgh'
        beer_id = 50

        self._require_login_and_auth(self.user3)
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=(room_name,)),
            data={'beer_id': beer_id}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('beer_id', res.attrs)

    def test_add_beer_user_not_host(self):
        self._require_login_and_auth(self.user2)
        self.assertNotEqual(self.user2, self.room_with_pass.host)

        beer = BeerFactory(name='user_not_host_beer')
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=('abcdefgh',)),
            data={'beer_id': beer.id}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode403Enum.PERMISSION_DENIED, res.codes)

    def test_add_beer_success(self):
        room_name = 'abcdefgh'
        beer_to_add = BeerFactory(name='test')
        beers_before = Beer.objects.filter(rooms__name=room_name).order_by('id')
        self.assertEqual(beers_before.count(), 4)

        self._require_login_and_auth(self.user3)
        response = self.client.put(
            reverse_lazy('rooms-detail-beers', args=(room_name,)),
            data={'beer_id': beer_to_add.id}
        )
        response_json = response.json()

        beers_after = Beer.objects.filter(rooms__name=room_name).order_by('rooms_through__order')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_json,
            BeerSerializer(beers_after, many=True).data
        )
        self.assertEqual(beers_after.count(), 5)

    def test_delete_no_id_in_url_parameters(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete(
            reverse_lazy('rooms-detail-beers', args=('abcdefgh',))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('beer_id')
        self.assertEqual(err.code, 'required')

    def test_delete_beer_room_doesnt_exist(self):
        self._require_login_and_auth(self.user3)
        response = self.client.delete(
            reverse_lazy('rooms-detail-beers', args=('XDDDD',)),
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_delete_beer_not_found_in_room(self):
        beer_id = 100

        self._require_login_and_auth(self.user3)
        response = self.client.delete(
            reverse_lazy('rooms-detail-beers', args=('abcdefgh',)) + f'?beer_id={beer_id}',
            data={'id': beer_id}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('beer_id')
        self.assertEqual(err.code, 'beer_not_in_room')

    def test_delete_beer_user_not_host(self):
        self.assertNotEqual(self.user2, self.room_with_pass.host)

        beer_id = 50

        self._require_login_and_auth(self.user2)
        response = self.client.delete(
            reverse_lazy('rooms-detail-beers', args=('abcdefgh',)) + f'?beer_id={beer_id}',
            data={'id': beer_id}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode403Enum.PERMISSION_DENIED, res.codes)

    def test_delete_beer_success(self):
        beer_id = 53
        query = f'?beer_id={beer_id}'

        self._require_login_and_auth(self.user3)
        response = self.client.delete(
            reverse_lazy('rooms-detail-beers', args=('abcdefgh',)) + query,
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

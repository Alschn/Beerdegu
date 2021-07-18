from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIClient

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
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user1 = User.objects.create_user(
            username='Test',
            password='!@#$%'
        )
        cls.user2 = User.objects.create_user(
            username='Test2',
            password='!@#$%'
        )
        cls.room = Room.objects.create(
            name='12345678',
            host=cls.user1,
            slots=4,
        )
        cls.room_with_pass = Room.objects.create(
            name='abcdefgh',
            host=User.objects.create_user(
                username='Test3',
                password='abcdef123@'
            ),
            password='password',
            slots=2,
        )

    # noinspection PyUnresolvedReferences
    def _require_login_and_auth(self, other: bool = False) -> None:
        if other:
            self.client.login(username='Test2', password='!@#$%')
            self.client.force_authenticate(self.user2)
        else:
            self.client.login(username='Test', password='!@#$%')
            self.client.force_authenticate(self.user1)

    def test_user_is_in_room_no_code_given(self):
        self._require_login_and_auth()
        response = self.client.get('/api/rooms/in')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual({'message': 'Missing code parameter in query!'}, to_json)

    def test_user_is_in_room_doesnt_exist(self):
        self._require_login_and_auth()
        response = self.client.get('/api/rooms/in?code=xd')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual({'message': 'Room with given code not found!'}, to_json)

    def test_user_is_not_in_room(self):
        self._require_login_and_auth(other=True)
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual({'message': 'User is not part of this room!'}, to_json)

    def test_user_is_in_room_and_host(self):
        self._require_login_and_auth()
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                'message': 'Test is in this room.',
                'is_host': True,
            },
            to_json
        )

    def test_user_is_in_room_not_host(self):
        self._require_login_and_auth(other=True)
        self.room.users.add(self.user2)
        response = self.client.get('/api/rooms/in?code=12345678')
        to_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            {
                'message': 'Test2 is in this room.',
                'is_host': False,
            },
            to_json
        )

    def test_join_room_not_found(self):
        self._require_login_and_auth()
        response = self.client.put('/api/rooms/aha/join', data={})
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room not found!'})

    def test_join_room_already_in(self):
        self._require_login_and_auth()
        response = self.client.put('/api/rooms/12345678/join', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'User is already in this room!'})

    def test_join_room_full(self):
        room = Room.objects.create(
            name='FULL',
            slots=1,
            host=self.user2
        )
        self._require_login_and_auth()
        self.assertEqual(room.slots, room.users.count())
        response = self.client.put('/api/rooms/FULL/join', data={})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.json(), {'message': f'Room FULL is full!'})

    def test_join_room_success(self):
        self._require_login_and_auth(other=True)
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/12345678/join', data={})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Joined room 12345678'})
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user2, r.users.all())

    def test_join_room_with_password_not_in_body(self):
        self._require_login_and_auth()
        response = self.client.put('/api/rooms/abcdefgh/join', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': 'Room abcdefgh is protected. No password found in body'})
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_password_invalid(self):
        self._require_login_and_auth()
        response = self.client.put('/api/rooms/abcdefgh/join', data={'password': '12345'})
        self.assertEqual(response.json(), {'message': 'Invalid password!'})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertNotIn(self.user1, self.room_with_pass.users.all())

    def test_join_room_with_password_success(self):
        self._require_login_and_auth()
        r = Room.objects.get(name='abcdefgh')
        self.assertEqual(r.users.count(), 1)
        response = self.client.put('/api/rooms/abcdefgh/join', data={'password': 'password'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Joined room abcdefgh'})
        self.assertEqual(r.users.count(), 2)
        self.assertIn(self.user1, r.users.all())

    def test_leave_room_not_found(self):
        self._require_login_and_auth()
        response = self.client.delete('/api/rooms/aha/leave')
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.json(), {'message': 'Room not found!'})

    def test_leave_room_not_in(self):
        self._require_login_and_auth(other=True)
        response = self.client.delete('/api/rooms/12345678/leave')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'message': f'Test2 is not inside this room!'})

    def test_leave_room_success(self):
        self._require_login_and_auth()
        r = Room.objects.get(name='12345678')
        self.assertEqual(r.users.count(), 1)
        response = self.client.delete('/api/rooms/12345678/leave')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), {'message': f'Test has left room 12345678!'})
        self.assertEqual(r.users.count(), 0)
        self.assertNotIn(self.user1, r.users.all())

    # to do ...

    def test_list_rooms(self):
        pass

    def test_create_room(self):
        pass

    def test_create_room_name_not_unique(self):
        pass

    def test_create_room_wrong_slots_number(self):
        pass

    def test_get_room_by_id(self):
        pass

    def test_update_room_by_id(self):
        pass

    def test_delete_room_by_id(self):
        pass

    def test_get_update_delete_room_doesnt_exist(self):
        pass

import unittest
from random import choice
from string import ascii_letters

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from beers.models import Hop
from beers.serializers import HopSerializer
from core.shared.unit_tests import APITestCase


class HopsAPIViewsTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.hop_simcoe = Hop.objects.create(name='Simcoe', country='USA')
        cls.hop_amarillo = Hop.objects.create(name='Amarillo', country='USA')

    def test_list_hops(self):
        response = self.client.get('/api/hops/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['results'],
            second=HopSerializer(Hop.objects.order_by('-id'), many=True).data
        )

    @unittest.skip('Currently disabled')
    def test_create_hop(self):
        self._require_login_and_auth()
        response = self.client.post('/api/hops/', {
            'name': 'Citra'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            first=response.json(),
            second=HopSerializer(Hop.objects.get(name='Citra')).data
        )

    @unittest.skip('Currently disabled')
    def test_create_hop_missing_data(self):
        self._require_login_and_auth()
        response = self.client.post('/api/hops/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_update_delete_hop_not_exists(self):
        response_get = self.client.get('/api/hops/1000/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # self._require_login_and_auth()
        # response_put = self.client.put('/api/hops/1000/', {})
        # self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_patch = self.client.patch('/api/hops/1000/', {})
        # self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_delete = self.client.delete('/api/hops/1000/')
        # self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_hop_by_id(self):
        response = self.client.get(f'/api/hops/{self.hop_amarillo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=HopSerializer(self.hop_amarillo).data
        )

    @unittest.skip('Currently disabled')
    def test_update_hop_by_id(self):
        self.assertIsNone(self.hop_amarillo.description)
        self._require_login_and_auth()
        response = self.client.patch(f'/api/hops/{self.hop_amarillo.id}/', data={
            'description': 'Amerykański chmiel uniwersalny'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hop_amarillo.refresh_from_db()
        self.assertEqual(self.hop_amarillo.description, 'Amerykański chmiel uniwersalny')

    @unittest.skip('Currently disabled')
    def test_update_hop_invalid_data(self):
        self._require_login_and_auth()
        response = self.client.patch(f'/api/hops/{self.hop_amarillo.id}/', data={
            'name': ''.join(choice(ascii_letters) for _ in range(31))
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip('Currently disabled')
    def test_delete_hop_by_id(self):
        self._require_login_and_auth()
        response = self.client.delete(f'/api/hops/{self.hop_simcoe.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Hop.objects.get(name='Simcoe')

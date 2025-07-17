import unittest
from random import choice
from string import ascii_letters

from django.core.exceptions import ObjectDoesNotExist
from drf_standardized_errors.openapi_serializers import (
    ValidationErrorEnum,
    ClientErrorEnum,
    ErrorCode404Enum
)
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from beers.models import Hop
from beers.serializers import HopSerializer
from core.shared.unit_tests import APITestCase, ExceptionResponse


class HopsAPIViewsTests(APITestCase):
    list_url = reverse_lazy('hops-list')

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.hop_simcoe = Hop.objects.create(name='Simcoe', country='USA')
        cls.hop_amarillo = Hop.objects.create(name='Amarillo', country='USA')

    def test_list_hops(self):
        queryset = Hop.objects.order_by('-id')

        response = self.client.get(self.list_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json['results'],
            HopSerializer(queryset, many=True).data
        )

    @unittest.skip('Currently disabled')
    def test_create_hop(self):
        self._require_login_and_auth()
        payload = {
            'name': 'Citra',
            'country': 'USA'
        }
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        hop = Hop.objects.get(name='Citra')
        self.assertEqual(
            response_json,
            HopSerializer(hop).data
        )

    @unittest.skip('Currently disabled')
    def test_create_hop_missing_data(self):
        self._require_login_and_auth()
        response = self.client.post(self.list_url, {})
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        self.assertIn('required', res.codes)

    def test_get_hop_does_not_exists(self):
        response = self.client.get(
            reverse_lazy('hops-detail', args=(1000,))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_get_hop_by_id(self):
        response = self.client.get(
            reverse_lazy('hops-detail', args=(self.hop_amarillo.id,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            HopSerializer(self.hop_amarillo).data
        )

    @unittest.skip('Currently disabled')
    def test_update_hop_by_id(self):
        payload = {
            'description': 'Amerykański chmiel uniwersalny'
        }
        self._require_login_and_auth()
        response = self.client.patch(
            reverse_lazy('hops-detail', args=(self.hop_amarillo.id,)),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hop_amarillo.refresh_from_db()
        self.assertEqual(self.hop_amarillo.description, payload['description'])

    @unittest.skip('Currently disabled')
    def test_update_hop_invalid_data(self):
        payload = {
            'name': ''.join(choice(ascii_letters) for _ in range(31))
        }
        self._require_login_and_auth()
        response = self.client.patch(
            reverse_lazy('hops-detail', args=(self.hop_amarillo.id,)),
            payload
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('name')
        self.assertEqual(err.code, 'max_length')

    @unittest.skip('Currently disabled')
    def test_delete_hop_by_id(self):
        self._require_login_and_auth()
        response = self.client.delete(
            reverse_lazy('hops-detail', args=(self.hop_simcoe.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Hop.objects.get(name='Simcoe')

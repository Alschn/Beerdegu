import unittest

from django.core.exceptions import ObjectDoesNotExist
from drf_standardized_errors.openapi_serializers import (
    ValidationErrorEnum,
    ClientErrorEnum,
    ErrorCode404Enum
)
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from beers.models import Brewery
from beers.serializers import BrewerySerializer
from core.shared.unit_tests import APITestCase, ExceptionResponse


class BreweriesAPIViewsTests(APITestCase):
    list_url = reverse_lazy('breweries-list')

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.brewery_pinta = Brewery.objects.create(name='Pinta', city='Wieprz')
        cls.brewery_inne_beczki = Brewery.objects.create(name='Inne Beczki')
        cls.brewery_to_delete = Brewery.objects.create(name='Jan Olbracht')

    def test_list_breweries(self):
        queryset = Brewery.objects.order_by('-id')

        response = self.client.get(self.list_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json['results'],
            BrewerySerializer(queryset, many=True).data
        )

    # todo: list breweries filters tests

    @unittest.skip('Currently disabled')
    def test_create_brewery(self):
        self._require_login_and_auth()
        payload = {
            'name': 'Zamkowy Cieszyn',
            'city': 'Cieszyn',
            'country': 'Polska',
        }
        response = self.client.post(self.list_url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        brewery = Brewery.objects.get(name=payload['name'])
        self.assertEqual(
            response.json(),
            BrewerySerializer(brewery).data
        )

    @unittest.skip('Currently disabled')
    def test_create_brewery_without_name(self):
        self._require_login_and_auth()
        payload = {
            'city': 'Olsztyn',
            'country': 'PL',
        }
        response = self.client.post(self.list_url, payload)
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('name')
        self.assertEqual(err.code, 'required')

    @unittest.skip('Currently disabled')
    def test_get_update_delete_brewery_not_exists(self):
        response = self.client.get(
            reverse_lazy('breweries-detail', args=(1000,))
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(res.type, ClientErrorEnum.CLIENT_ERROR)
        self.assertIn(ErrorCode404Enum.NOT_FOUND, res.codes)

    def test_get_brewery_by_id(self):
        response = self.client.get(
            reverse_lazy('breweries-detail', args=(self.brewery_pinta.id,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            BrewerySerializer(self.brewery_pinta).data
        )

    @unittest.skip('Currently disabled')
    def test_update_brewery_by_id(self):
        self.assertEqual(self.brewery_pinta.city, 'Wieprz')
        self._require_login_and_auth()
        payload = {
            'city': 'Warszawa'
        }
        response = self.client.patch(
            reverse_lazy('breweries-detail', args=(self.brewery_pinta.id,)),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.brewery_pinta.refresh_from_db()
        self.assertEqual(self.brewery_pinta.city, payload['city'])

    @unittest.skip('Currently disabled')
    def test_update_brewery_invalid_data(self):
        self._require_login_and_auth()
        response = self.client.put(
            reverse_lazy('breweries-detail', args=(self.brewery_pinta.id,)),
            data={}
        )
        res = ExceptionResponse.from_response(response)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(res.type, ValidationErrorEnum.VALIDATION_ERROR)
        err = res.get_error_by_attr('name')
        self.assertEqual(err.code, 'required')

    @unittest.skip('Currently disabled')
    def test_delete_brewery_by_id(self):
        lookup_id = self.brewery_to_delete.id
        self._require_login_and_auth()
        response = self.client.delete(
            reverse_lazy('breweries-detail', args=(lookup_id,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Brewery.objects.get(id=lookup_id)

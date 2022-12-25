import unittest

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from beers.models import Beer, BeerStyle, Hop, Brewery
from beers.serializers import BrewerySerializer
from core.shared.unit_tests import APITestCase


class BreweriesAPIViewsTests(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.brewery_pinta = Brewery.objects.create(name='Pinta', city='Wieprz')
        cls.brewery_inne_beczki = Brewery.objects.create(name='Inne Beczki')
        cls.brewery_to_delete = Brewery.objects.create(name='Jan Olbracht')

    def test_list_breweries(self):
        response = self.client.get('/api/breweries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['results'],
            second=BrewerySerializer(Brewery.objects.order_by('-id'), many=True).data
        )

    @unittest.skip('Currently disabled')
    def test_create_brewery(self):
        self._require_login_and_auth()
        response = self.client.post('/api/breweries/', {
            'name': 'Zamkowy Cieszyn',
            'city': 'Cieszyn',
            'country': 'Polska',
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            first=response.json(),
            second=BrewerySerializer(Brewery.objects.get(name='Zamkowy Cieszyn')).data
        )

    @unittest.skip('Currently disabled')
    def test_create_brewery_without_name(self):
        self._require_login_and_auth()
        response = self.client.post('/api/breweries/', {
            'city': 'Olsztyn',
            'country': 'Polska',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip('Currently disabled')
    def test_get_update_delete_brewery_not_exists(self):
        response_get = self.client.get('/api/breweries/1000/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # self._require_login_and_auth()
        # response_put = self.client.put('/api/breweries/1000/', {})
        # self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_patch = self.client.patch('/api/breweries/1000/', {})
        # self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_delete = self.client.delete('/api/breweries/1000/')
        # self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_brewery_by_id(self):
        response = self.client.get(f'/api/breweries/{self.brewery_inne_beczki.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BrewerySerializer(self.brewery_inne_beczki).data)

    @unittest.skip('Currently disabled')
    def test_update_brewery_by_id(self):
        self.assertEqual(self.brewery_pinta.city, 'Wieprz')
        self._require_login_and_auth()
        response = self.client.patch(f'/api/breweries/{self.brewery_pinta.id}/', data={
            'city': 'Warszawa'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.brewery_pinta.refresh_from_db()
        self.assertEqual(self.brewery_pinta.city, 'Warszawa')

    @unittest.skip('Currently disabled')
    def test_update_brewery_invalid_data(self):
        self._require_login_and_auth()
        response = self.client.put(f'/api/breweries/{self.brewery_pinta.id}/', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'name': ['This field is required.']})

    @unittest.skip('Currently disabled')
    def test_delete_brewery_by_id(self):
        lookup_id = self.brewery_to_delete.id
        self._require_login_and_auth()
        response = self.client.delete(f'/api/breweries/{lookup_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Brewery.objects.get(id=lookup_id)

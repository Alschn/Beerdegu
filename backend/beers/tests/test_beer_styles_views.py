import unittest
from random import choice
from string import ascii_letters

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from beers.models import BeerStyle
from beers.serializers import BeerStyleSerializer
from core.shared.unit_tests import APITestCase


class BeerStylesAPIViewsTests(APITestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.style_ipa = BeerStyle.objects.create(name='India Pale Ale')
        cls.style_apa = BeerStyle.objects.create(name='American Pale Ale')
        cls.beer_style_to_delete = BeerStyle.objects.create(name='DDH APA')

    def test_list_beer_styles(self):
        response = self.client.get('/api/styles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json()['results'],
            second=BeerStyleSerializer(BeerStyle.objects.order_by('-id'), many=True).data
        )

    @unittest.skip('Currently disabled')
    def test_create_beer_style(self):
        self._require_login_and_auth()
        response = self.client.post('/api/styles/', {
            'name': 'DDH Hazy IPA'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            first=response.json(),
            second=BeerStyleSerializer(BeerStyle.objects.get(name='DDH Hazy IPA')).data
        )

    @unittest.skip('Currently disabled')
    def test_create_beer_style_no_name(self):
        self._require_login_and_auth()
        response = self.client.post('/api/styles/', {
            'description': 'Dry hopped'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_update_delete_beer_style_not_exists(self):
        response_get = self.client.get('/api/styles/10/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # self._require_login_and_auth()
        # response_put = self.client.put('/api/styles/10/', {})
        # self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_patch = self.client.patch('/api/styles/10/', {})
        # self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_delete = self.client.delete('/api/styles/10/')
        # self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    @unittest.skip('Currently disabled')
    def test_get_beer_style_by_id(self):
        response = self.client.get(f'/api/styles/{self.style_apa.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=BeerStyleSerializer(self.style_apa).data
        )

    @unittest.skip('Currently disabled')
    def test_update_beer_style_by_id(self):
        self._require_login_and_auth()
        response = self.client.put(f'/api/styles/{self.style_apa.id}/', data={
            'name': 'APA',
            'description': 'Very nice beer style',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.style_apa.refresh_from_db()
        self.assertEqual(response.json(), BeerStyleSerializer(self.style_apa).data)

    @unittest.skip('Currently disabled')
    def test_update_beer_style_invalid_data(self):
        self._require_login_and_auth()
        response = self.client.patch(f'/api/styles/{self.style_ipa.id}/', data={
            'description': ''.join(choice(ascii_letters) for _ in range(1001)),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip('Currently disabled')
    def test_delete_beer_style_by_id(self):
        self._require_login_and_auth()
        response = self.client.delete(f'/api/styles/{self.beer_style_to_delete.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            BeerStyle.objects.get(name='DDH APA')

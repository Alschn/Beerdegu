import unittest
from random import choice
from string import ascii_letters

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.reverse import reverse_lazy

from beers.models import BeerStyle
from beers.serializers import BeerStyleListSerializer, BeerStyleDetailSerializer
from core.shared.factories import BeerStyleFactory
from core.shared.unit_tests import APITestCase


class BeerStylesAPIViewsTests(APITestCase):
    styles_url = reverse_lazy('styles-list')

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.style_ipa = BeerStyleFactory(name='IPA')
        cls.style_apa = BeerStyleFactory(name='APA')
        cls.beer_style_to_delete = BeerStyleFactory(name='DDH APA')

    def test_list_beer_styles(self):
        queryset = BeerStyle.objects.order_by('-id')

        response = self.client.get(self.styles_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json['results'],
            BeerStyleListSerializer(queryset, many=True).data
        )

    @unittest.skip('Currently disabled')
    def test_create_beer_style(self):
        self._require_login_and_auth()
        response = self.client.post(self.styles_url, {
            'name': 'DDH Hazy IPA'
        })
        response_json = response.json()
        beer_style = BeerStyle.objects.get(name='DDH Hazy IPA')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response_json,
            BeerStyleListSerializer(beer_style).data
        )

    @unittest.skip('Currently disabled')
    def test_create_beer_style_no_name(self):
        self._require_login_and_auth()
        response = self.client.post(self.styles_url, {
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

    def test_get_beer_style_by_id(self):
        response = self.client.get(
            reverse_lazy('styles-detail', args=(self.style_apa.id,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response_json,
            BeerStyleDetailSerializer(self.style_apa).data
        )

    @unittest.skip('Currently disabled')
    def test_update_beer_style_by_id(self):
        self._require_login_and_auth()
        payload = {
            'name': 'APA',
            'description': 'Very nice beer style',
        }
        response = self.client.put(
            reverse_lazy('styles-detail', args=(self.style_apa.id,)),
            data=payload
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.style_apa.refresh_from_db()
        self.assertEqual(
            response_json,
            BeerStyleDetailSerializer(self.style_apa).data
        )

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

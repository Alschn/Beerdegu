import unittest
from random import choice
from string import ascii_letters

from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status

from beers.models import (
    Beer, BeerStyle,
    Hop, Brewery
)
from beers.serializers import (
    BeerDetailedSerializer,
    BeerSerializer,
)
from core.shared.unit_tests import APITestCase


class BeersAPIViewsTest(APITestCase):

    @classmethod
    def setUpTestData(cls) -> None:
        super().setUpTestData()
        cls.style_ipa = BeerStyle.objects.create(name='India Pale Ale')
        cls.style_apa = BeerStyle.objects.create(name='American Pale Ale')
        cls.hop_simcoe = Hop.objects.create(name='Simcoe', country='USA')
        cls.hop_amarillo = Hop.objects.create(name='Amarillo', country='USA')
        cls.brewery_pinta = Brewery.objects.create(name='Pinta', city='Wieprz')
        cls.brewery_inne_beczki = Brewery.objects.create(name='Inne Beczki')
        Beer.objects.bulk_create([
            Beer(
                name='Jungle IPA', brewery=cls.brewery_inne_beczki,
                percentage=6.0, volume_ml=500, style=cls.style_ipa
            ),
            Beer(
                name='Zissou APA', brewery=cls.brewery_inne_beczki,
                percentage=5, volume_ml=500
            ),
            Beer(
                name='Hoppy Crew: Who Snaps First', brewery=cls.brewery_pinta,
                percentage=8, volume_ml=500
            )
        ])
        cls.beer_to_update = Beer.objects.create(
            name='PanIIPAni', percentage=6.7, volume_ml=500,
            style=cls.style_ipa, brewery=cls.brewery_pinta
        )
        cls.beer_to_delete = Beer.objects.create(
            name='A Ja Pale Ale', percentage=5, volume_ml=500,
            style=cls.style_apa, brewery=cls.brewery_pinta
        )

    def test_list_beers(self):
        response = self.client.get('/api/beers/')
        json_response = response.json()
        beers = Beer.objects.order_by('-id')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(json_response['count'], beers.count())
        self.assertEqual(
            first=BeerDetailedSerializer(beers, many=True).data,
            second=json_response['results']
        )

    def test_create_beer(self):
        self._require_login_and_auth()
        response = self.client.post('/api/beers/', data={
            'name': "a'la Grodziskie",
            'percentage': 5,
            'volume_ml': 500,
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            response.json(),
            BeerSerializer(Beer.objects.get(name="a'la Grodziskie")).data
        )

    def test_create_beer_missing_data(self):
        self._require_login_and_auth()
        response = self.client.post('/api/beers/', data={
            'name': "Random name",
            'volume_ml': 750,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('percentage', response.json())

    def test_create_beer_negative_percentage(self):
        self._require_login_and_auth()
        response = self.client.post('/api/beers/', data={
            'name': "Negative",
            'percentage': -1,
            'volume_ml': 500,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('percentage', response.json())

    # todo: more create beer tests (including base64 image upload)

    def test_retrieve_beer(self):
        beer = Beer.objects.create(name='Kwas Theta', percentage=10.2, volume_ml=500)
        response = self.client.get(f'/api/beers/{beer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BeerSerializer(beer).data)

    # todo: more retrieve beer tests

    def test_get_update_delete_beer_not_exists(self):
        response_get = self.client.get('/api/beers/200/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        # self._require_login_and_auth()
        # response_put = self.client.put('/api/beers/200/', {})
        # self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_patch = self.client.patch('/api/beers/200/', {})
        # self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)
        #
        # response_delete = self.client.delete('/api/beers/200/')
        # self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    @unittest.skip('Currently disabled')
    def test_update_beer_by_id(self):
        self._require_login_and_auth()
        self.assertIsNone(self.beer_to_update.description)
        response = self.client.patch(f"/api/beers/{self.beer_to_update.id}/", {
            "description": 'Very nice beer',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        beer = Beer.objects.get(name='PanIIPAni')
        self.assertEqual(beer.description, "Very nice beer")

    @unittest.skip('Currently disabled')
    def test_update_beer_too_long_data(self):
        self._require_login_and_auth()
        response = self.client.patch(f"/api/beers/{self.beer_to_update.id}/", {
            "name": ''.join(choice(ascii_letters) for _ in range(101)),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    @unittest.skip('Currently disabled')
    def test_delete_beer_by_id(self):
        self._require_login_and_auth()
        qs_len_before = Beer.objects.all().count()
        lookup_id = self.beer_to_delete.id
        response = self.client.delete(f"/api/beers/{lookup_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(qs_len_before - 1, Beer.objects.all().count())
        with self.assertRaises(ObjectDoesNotExist):
            Beer.objects.get(id=lookup_id)

    # todo: filtering unit tests

    def test_list_beers_filter_name_icontains(self):
        pass

    def test_list_beers_filter_name_not_contains(self):
        pass

    def test_list_beers_filter_brewery(self):
        pass

    def test_list_beers_filter_multiple_breweries(self):
        pass

    def test_list_beers_filter_brewery_does_not_exist(self):
        pass

    def test_list_beers_filter_brewery_name_icontains(self):
        pass

    def test_list_beers_filter_style(self):
        pass

    def test_list_beers_filter_multiple_styles(self):
        pass

    def test_list_beers_filter_style_does_not_exist(self):
        pass

    def test_list_beers_filter_percentage_gte(self):
        pass

    def test_list_beers_filter_percentage_lte(self):
        pass

    def test_list_beers_filter_percentage_range(self):
        pass

    def test_list_beers_filter_percentage_invalid_range(self):
        pass

    def test_list_beers_filter_volume_ml_gte(self):
        pass

    def test_list_beers_filter_volume_ml_lte(self):
        pass

    def test_list_beers_filter_volume_ml_range(self):
        pass

    def test_list_beers_filter_volume_ml_invalid_range(self):
        pass

    def test_list_beers_filter_hop_rate_gte(self):
        pass

    def test_list_beers_filter_hop_rate_lte(self):
        pass

    def test_list_beers_filter_hop_rate_range(self):
        pass

    def test_list_beers_filter_hop_rate_invalid_range(self):
        pass

    def test_list_beers_filter_ibu_gte(self):
        pass

    def test_list_beers_filter_ibu_lte(self):
        pass

    def test_list_beers_filter_ibu_range(self):
        pass

    def test_list_beers_filter_ibu_invalid_range(self):
        pass

    def test_list_beers_filter_extract_gte(self):
        pass

    def test_list_beers_filter_extract_lte(self):
        pass

    def test_list_beers_filter_extract_range(self):
        pass

    def test_list_beers_filter_extract_invalid_range(self):
        pass

    def test_list_beers_filter_hop(self):
        pass

    def test_list_beers_filter_multiple_hops(self):
        pass

    def test_list_beers_filter_hop_does_not_exist(self):
        pass

    def test_list_beers_filter_hops_name_icontains(self):
        pass

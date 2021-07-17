from random import choice
from string import ascii_letters

from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APIClient

from beers.models import Beer, BeerStyle, Hop, Brewery
from beers.serializers import (
    DetailedBeerSerializer, BeerSerializer,
    HopSerializer, StyleSerializer, BrewerySerializer,
)


class BeersAPIViewsTest(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

    @classmethod
    def setUpTestData(cls) -> None:
        cls.user = User.objects.create_user(
            username='Test',
            password='!@#$%'
        )
        cls.token = Token.objects.get_or_create(user=cls.user)
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
        cls.brewery_to_delete = Brewery.objects.create(name='Jan Olbracht')
        cls.beer_style_to_delete = BeerStyle.objects.create(name='DDH APA')

    def _require_login_and_auth(self) -> None:
        self.client.login(username='Test', password='!@#$%')
        # noinspection PyUnresolvedReferences
        self.client.force_authenticate(self.user)

    def test_list_beers(self):
        response = self.client.get('/api/beers/')
        json_response = response.json()
        beers = Beer.objects.all()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(json_response), beers.count())
        self.assertEqual(
            first=DetailedBeerSerializer(beers, many=True).data,
            second=json_response
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

    def test_create_beer_negative_percentage(self):
        self._require_login_and_auth()
        response = self.client.post('/api/beers/', data={
            'name': "Negative",
            'percentage': -1,
            'volume_ml': 500,
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_beer_by_id(self):
        beer = Beer.objects.create(name='Kwas Theta', percentage=10.2, volume_ml=500)
        response = self.client.get(f'/api/beers/{beer.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BeerSerializer(beer).data)

    def test_get_update_delete_beer_not_exists(self):
        response_get = self.client.get('/api/beers/200/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        self._require_login_and_auth()
        response_put = self.client.put('/api/beers/200/', {})
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        response_patch = self.client.patch('/api/beers/200/', {})
        self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.client.delete('/api/beers/200/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_update_beer_by_id(self):
        self._require_login_and_auth()
        self.assertIsNone(self.beer_to_update.description)
        response = self.client.patch(f"/api/beers/{self.beer_to_update.id}/", {
            "description": 'Very nice beer',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        beer = Beer.objects.get(name='PanIIPAni')
        self.assertEqual(beer.description, "Very nice beer")

    def test_update_beer_too_long_data(self):
        self._require_login_and_auth()
        response = self.client.patch(f"/api/beers/{self.beer_to_update.id}/", {
            "name": ''.join(choice(ascii_letters) for _ in range(101)),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_beer_by_id(self):
        self._require_login_and_auth()
        qs_len_before = Beer.objects.all().count()
        lookup_id = self.beer_to_delete.id
        response = self.client.delete(f"/api/beers/{lookup_id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(qs_len_before - 1, Beer.objects.all().count())
        with self.assertRaises(ObjectDoesNotExist):
            Beer.objects.get(id=lookup_id)

    def test_list_beer_styles(self):
        response = self.client.get('/api/styles/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=StyleSerializer(BeerStyle.objects.all(), many=True).data
        )

    def test_create_beer_style(self):
        self._require_login_and_auth()
        response = self.client.post('/api/styles/', {
            'name': 'DDH Hazy IPA'
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(
            first=response.json(),
            second=StyleSerializer(BeerStyle.objects.get(name='DDH Hazy IPA')).data
        )

    def test_create_beer_style_no_name(self):
        self._require_login_and_auth()
        response = self.client.post('/api/styles/', {
            'description': 'Dry hopped'
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_update_delete_beer_style_not_exists(self):
        response_get = self.client.get('/api/styles/10/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        self._require_login_and_auth()
        response_put = self.client.put('/api/styles/10/', {})
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        response_patch = self.client.patch('/api/styles/10/', {})
        self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.client.delete('/api/styles/10/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_beer_style_by_id(self):
        response = self.client.get(f'/api/styles/{self.style_apa.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=StyleSerializer(self.style_apa).data
        )

    def test_update_beer_style_by_id(self):
        response = self.client.put(f'/api/styles/{self.style_apa.id}/', data={
            'name': 'APA',
            'description': 'Very nice beer style',
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.style_apa.refresh_from_db()
        self.assertEqual(response.json(), StyleSerializer(self.style_apa).data)

    def test_update_beer_style_invalid_data(self):
        response = self.client.patch(f'/api/styles/{self.style_ipa.id}/', data={
            'description': ''.join(choice(ascii_letters) for _ in range(1001)),
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_beer_style_by_id(self):
        self._require_login_and_auth()
        response = self.client.delete(f'/api/styles/{self.beer_style_to_delete.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            BeerStyle.objects.get(name='DDH APA')

    def test_list_hops(self):
        response = self.client.get('/api/hops/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=HopSerializer(Hop.objects.all(), many=True).data
        )

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

    def test_create_hop_missing_data(self):
        self._require_login_and_auth()
        response = self.client.post('/api/hops/', {})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_update_delete_hop_not_exists(self):
        response_get = self.client.get('/api/hops/1000/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        self._require_login_and_auth()
        response_put = self.client.put('/api/hops/1000/', {})
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        response_patch = self.client.patch('/api/hops/1000/', {})
        self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.client.delete('/api/hops/1000/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_hop_by_id(self):
        response = self.client.get(f'/api/hops/{self.hop_amarillo.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=HopSerializer(self.hop_amarillo).data
        )

    def test_update_hop_by_id(self):
        self.assertIsNone(self.hop_amarillo.description)
        response = self.client.patch(f'/api/hops/{self.hop_amarillo.id}/', data={
            'description': 'Amerykański chmiel uniwersalny'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.hop_amarillo.refresh_from_db()
        self.assertEqual(self.hop_amarillo.description, 'Amerykański chmiel uniwersalny')

    def test_update_hop_invalid_data(self):
        response = self.client.patch(f'/api/hops/{self.hop_amarillo.id}/', data={
            'name': ''.join(choice(ascii_letters) for _ in range(31))
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_delete_hop_by_id(self):
        response = self.client.delete(f'/api/hops/{self.hop_simcoe.id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Hop.objects.get(name='Simcoe')

    def test_list_breweries(self):
        response = self.client.get('/api/breweries/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            first=response.json(),
            second=BrewerySerializer(Brewery.objects.all(), many=True).data
        )

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

    def test_create_brewery_without_name(self):
        self._require_login_and_auth()
        response = self.client.post('/api/breweries/', {
            'city': 'Olsztyn',
            'country': 'Polska',
        })
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_get_update_delete_brewery_not_exists(self):
        response_get = self.client.get('/api/breweries/1000/')
        self.assertEqual(response_get.status_code, status.HTTP_404_NOT_FOUND)

        self._require_login_and_auth()
        response_put = self.client.put('/api/breweries/1000/', {})
        self.assertEqual(response_put.status_code, status.HTTP_404_NOT_FOUND)

        response_patch = self.client.patch('/api/breweries/1000/', {})
        self.assertEqual(response_patch.status_code, status.HTTP_404_NOT_FOUND)

        response_delete = self.client.delete('/api/breweries/1000/')
        self.assertEqual(response_delete.status_code, status.HTTP_404_NOT_FOUND)

    def test_get_brewery_by_id(self):
        response = self.client.get(f'/api/breweries/{self.brewery_inne_beczki.id}/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), BrewerySerializer(self.brewery_inne_beczki).data)

    def test_update_brewery_by_id(self):
        self.assertEqual(self.brewery_pinta.city, 'Wieprz')
        response = self.client.patch(f'/api/breweries/{self.brewery_pinta.id}/', data={
            'city': 'Warszawa'
        })
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.brewery_pinta.refresh_from_db()
        self.assertEqual(self.brewery_pinta.city, 'Warszawa')

    def test_update_brewery_invalid_data(self):
        self.assertEqual(self.brewery_pinta.city, 'Wieprz')
        response = self.client.put(f'/api/breweries/{self.brewery_pinta.id}/', data={})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.json(), {'name': ['This field is required.']})

    def test_delete_brewery_by_id(self):
        lookup_id = self.brewery_to_delete.id
        response = self.client.delete(f'/api/breweries/{lookup_id}/')
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        with self.assertRaises(ObjectDoesNotExist):
            Brewery.objects.get(id=lookup_id)


class BeersModelsTest(TestCase):
    @classmethod
    def setUpTestData(cls) -> None:
        cls.brewery = Brewery.objects.create(name='Warmia')

    def test_Beer_to_string(self):
        beer_with_brewery = Beer.objects.create(
            name='West Coast IPA', brewery=self.brewery,
            percentage=5, volume_ml=500
        )
        beer_without_brewery = Beer.objects.create(
            name='West Coast IPA',
            percentage=5, volume_ml=500
        )
        self.assertEqual(str(beer_with_brewery), "West Coast IPA 5% 500ml, Browar Warmia")
        self.assertEqual(str(beer_without_brewery), "West Coast IPA 5% 500ml")

    def test_BeerStyle_to_string(self):
        beer_style = BeerStyle.objects.create(name='Russian Imperial Stout')
        self.assertEqual(str(beer_style), "Russian Imperial Stout")

    def test_Hop_to_string(self):
        hop = BeerStyle.objects.create(name='Marynka')
        self.assertEqual(str(hop), "Marynka")

    def test_Brewery_to_string(self):
        self.assertEqual(str(self.brewery), "Browar Warmia")

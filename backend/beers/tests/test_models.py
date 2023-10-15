from django.test import TestCase

from beers.models import Beer, BeerStyle, Brewery


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
        self.assertEqual(str(beer_with_brewery), "West Coast IPA 5% 500ml, Warmia")
        self.assertEqual(str(beer_without_brewery), "West Coast IPA 5% 500ml")

    def test_BeerStyle_to_string(self):
        beer_style = BeerStyle.objects.create(name='Russian Imperial Stout')
        self.assertEqual(str(beer_style), "Russian Imperial Stout")

    def test_Hop_to_string(self):
        hop = BeerStyle.objects.create(name='Marynka')
        self.assertEqual(str(hop), "Marynka")

    def test_Brewery_to_string(self):
        self.assertEqual(str(self.brewery), "Warmia")

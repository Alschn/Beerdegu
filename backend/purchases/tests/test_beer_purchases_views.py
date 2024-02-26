import datetime

import freezegun
from django.utils import timezone
from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from core.shared.factories import BeerPurchaseFactory, UserFactory, DEFAULT_USER_FACTORY_PASSWORD, BeerFactory
from purchases.models import BeerPurchase
from purchases.serializers.beer_purchase import BeerPurchaseSerializer, BeerPurchaseCreateSerializer


class BeerPurchasesViewsTests(APITestCase):
    list_url = reverse_lazy('beer-purchases-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username='test')

    def _require_login(self):
        self.client.login(username=self.user.username, password=DEFAULT_USER_FACTORY_PASSWORD)
        self.client.force_authenticate(self.user)

    def test_list_purchases(self):
        BeerPurchaseFactory.create_batch(3, sold_to=self.user)
        BeerPurchaseFactory.create_batch(2)
        queryset = BeerPurchase.objects.filter(sold_to=self.user).order_by('-purchased_at')

        self._require_login()
        response = self.client.get(self.list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(response_json['count'], queryset.count())
        self.assertEqual(
            response_json['results'],
            BeerPurchaseSerializer(queryset, many=True).data
        )

    def test_list_purchases_not_authenticated(self):
        BeerPurchaseFactory.create_batch(2, sold_to=self.user)
        response = self.client.get(self.list_url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_list_purchases_filter_beer(self):
        BeerPurchaseFactory.create_batch(2, sold_to=self.user)
        purchase = BeerPurchaseFactory(sold_to=self.user)
        beer = purchase.beer

        queryset = BeerPurchase.objects.filter(
            sold_to=self.user, beer=beer
        ).order_by('-purchased_at')

        self._require_login()
        response = self.client.get(self.list_url, {'beer': beer.id})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(response_json['count'], 1)
        self.assertEqual(
            response_json['results'],
            BeerPurchaseSerializer(queryset, many=True).data
        )

    def test_list_purchases_filter_multiple_beers(self):
        BeerPurchaseFactory.create_batch(2, sold_to=self.user)
        purchase1, purchase2 = BeerPurchaseFactory.create_batch(2, sold_to=self.user)
        beer1, beer2 = purchase1.beer, purchase2.beer

        queryset = BeerPurchase.objects.filter(
            sold_to=self.user, beer__in=[beer1, beer2]
        ).order_by('-purchased_at')

        self._require_login()
        response = self.client.get(self.list_url, {'beer': f'{beer1.id},{beer2.id}'})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(response_json['count'], queryset.count())
        self.assertEqual(
            response_json['results'],
            BeerPurchaseSerializer(queryset, many=True).data
        )

    def test_list_purchases_filter_packaging(self):
        BeerPurchaseFactory.create_batch(2, sold_to=self.user, packaging=BeerPurchase.Packaging.BOTTLE)
        BeerPurchaseFactory(sold_to=self.user, packaging=BeerPurchase.Packaging.CAN)

        queryset = BeerPurchase.objects.filter(
            sold_to=self.user, packaging=BeerPurchase.Packaging.CAN
        ).order_by('-purchased_at')

        self._require_login()
        response = self.client.get(self.list_url, {'packaging': str(BeerPurchase.Packaging.CAN)})
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response_json = response.json()
        self.assertEqual(response_json['count'], 1)
        self.assertEqual(
            response_json['results'],
            BeerPurchaseSerializer(queryset, many=True).data
        )

    # todo: test filter price, volume_ml, purchased_at
    # todo: test order by purchased_at, price

    def test_retrieve_purchase(self):
        purchase = BeerPurchaseFactory(sold_to=self.user)

        self._require_login()
        response = self.client.get(
            reverse_lazy('beer-purchases-detail', kwargs={'pk': purchase.id})
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            response.json(),
            BeerPurchaseSerializer(purchase).data
        )

    def test_retrieve_purchase_not_authenticated(self):
        purchase = BeerPurchaseFactory(sold_to=self.user)
        response = self.client.get(
            reverse_lazy('beer-purchases-detail', kwargs={'pk': purchase.id})
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_retrieve_purchase_other_user(self):
        purchase = BeerPurchaseFactory()

        self._require_login()
        response = self.client.get(
            reverse_lazy('beer-purchases-detail', kwargs={'pk': purchase.id})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_retrieve_purchase_not_found(self):
        self._require_login()
        response = self.client.get(
            reverse_lazy('beer-purchases-detail', kwargs={'pk': 696969})
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_create_purchase(self):
        beer = BeerFactory()
        data = {
            'beer': beer.id,
            'packaging': BeerPurchase.Packaging.CAN,
            'price': 10.0,
            'volume_ml': 500,
            'purchased_at': '2021-01-01',
        }
        self._require_login()
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        purchase = BeerPurchase.objects.get(id=response_json['id'])
        self.assertEqual(
            response_json,
            BeerPurchaseCreateSerializer(purchase).data
        )

    @freezegun.freeze_time('2024-01-01')
    def test_create_purchase_without_purchased_at(self):
        beer = BeerFactory()
        data = {
            'beer': beer.id,
            'packaging': BeerPurchase.Packaging.CAN,
            'price': 10.0,
            'volume_ml': 500,
        }
        self._require_login()
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        response_json = response.json()
        purchase = BeerPurchase.objects.get(id=response_json['id'])
        self.assertEqual(purchase.purchased_at, timezone.now().date())

    def test_create_purchase_not_authenticated(self):
        response = self.client.post(self.list_url, {})
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

    def test_create_purchase_invalid_data(self):
        future_date = timezone.now().date() + datetime.timedelta(days=1)
        data = {
            'beer': 500,
            'packaging': 'invalid',
            'price': -10.0,
            'volume_ml': -500,
            'purchased_at': future_date.strftime('%Y-%m-%d'),
        }

        self._require_login()
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_json = response.json()
        self.assertIn('beer', response_json)
        self.assertIn('packaging', response_json)
        self.assertIn('price', response_json)
        self.assertIn('volume_ml', response_json)
        self.assertIn('purchased_at', response_json)

    def test_create_purchase_missing_data(self):
        data = {}
        self._require_login()
        response = self.client.post(self.list_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        response_json = response.json()
        self.assertIn('beer', response_json)
        self.assertIn('packaging', response_json)
        self.assertIn('price', response_json)
        self.assertIn('volume_ml', response_json)

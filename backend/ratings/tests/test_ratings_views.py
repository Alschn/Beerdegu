from rest_framework import status
from rest_framework.reverse import reverse_lazy
from rest_framework.test import APITestCase

from core.shared.factories import (
    UserFactory,
    RatingFactory,
    BeerFactory,
    BeerPurchaseFactory,
    RoomFactory,
    DEFAULT_USER_FACTORY_PASSWORD,
)
from ratings.models import Rating
from ratings.serializers import (
    RatingListSerializer,
    RatingDetailSerializer
)


class RatingsViewSetTests(APITestCase):
    list_url = reverse_lazy('ratings-list')

    @classmethod
    def setUpTestData(cls):
        cls.user = UserFactory(username='test')

    def _require_login(self):
        self.client.login(username=self.user.username, password=DEFAULT_USER_FACTORY_PASSWORD)
        self.client.force_authenticate(self.user)

    def test_list_ratings(self):
        RatingFactory.create_batch(3, added_by=self.user)

        queryset = Rating.objects.filter(added_by=self.user).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())
        self.assertEqual(
            response_json['results'],
            RatingListSerializer(queryset, many=True).data
        )

    def test_list_ratings_filter_beer(self):
        beer = BeerFactory()
        RatingFactory.create_batch(3, added_by=self.user, beer_purchase=None)
        RatingFactory.create_batch(2, added_by=self.user, beer=beer, beer_purchase=None)

        queryset = Rating.objects.filter(
            added_by=self.user, beer=beer
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'beer': beer.id})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_beer_not_exists(self):
        self._require_login()
        response = self.client.get(self.list_url, {'beer': 69})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer', response_json)

    def test_list_ratings_filter_beer_in(self):
        beer1, beer2 = BeerFactory.create_batch(2)
        RatingFactory.create_batch(3, added_by=self.user, beer_purchase=None)
        RatingFactory.create(added_by=self.user, beer=beer1, beer_purchase=None)
        RatingFactory.create(added_by=self.user, beer=beer2, beer_purchase=None)

        queryset = Rating.objects.filter(
            added_by=self.user, beer__in=[beer1, beer2]
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'beer__in': f'{beer1.id},{beer2.id}'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_beer_in_not_exists(self):
        self._require_login()
        response = self.client.get(self.list_url, {'beer': '69,420'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer', response_json)

    def test_list_ratings_filter_room(self):
        room = RoomFactory(host=self.user)
        RatingFactory.create_batch(3, added_by=self.user, room=None)
        RatingFactory.create_batch(2, added_by=self.user, room=room)

        queryset = Rating.objects.filter(
            added_by=self.user, room=room
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'room': room.id})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_room_not_exists(self):
        self._require_login()
        response = self.client.get(self.list_url, {'room': '2137'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('room', response_json)

    def test_list_ratings_filter_room_in(self):
        room1, room2 = RoomFactory.create_batch(2, host=self.user)
        RatingFactory.create_batch(3, added_by=self.user, room=None)
        RatingFactory.create(added_by=self.user, room=room1)
        RatingFactory.create(added_by=self.user, room=room2)

        queryset = Rating.objects.filter(
            added_by=self.user, room__in=[room1, room2]
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'room__in': f'{room1.id},{room2.id}'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_room_in_not_exists(self):
        self._require_login()
        response = self.client.get(self.list_url, {'room__in': '21,37'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('room__in', response_json)

    def test_list_ratings_filter_note_gte(self):
        RatingFactory.create_batch(3, added_by=self.user, note=8)
        RatingFactory.create_batch(2, added_by=self.user, note=7)
        RatingFactory.create(added_by=self.user, note=6)

        note = 7
        queryset = Rating.objects.filter(
            added_by=self.user, note__gte=note
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'note__gte': note})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_note_lte(self):
        RatingFactory.create_batch(3, added_by=self.user, note=8)
        RatingFactory.create_batch(2, added_by=self.user, note=7)
        RatingFactory.create(added_by=self.user, note=6)

        note = 7
        queryset = Rating.objects.filter(
            added_by=self.user, note__lte=note
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'note__lte': note})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_note_gt(self):
        RatingFactory.create_batch(2, added_by=self.user, note=8)
        RatingFactory.create(added_by=self.user, note=7)

        note = 7
        queryset = Rating.objects.filter(
            added_by=self.user, note__gt=note
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'note__gt': note})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_note_lt(self):
        RatingFactory.create_batch(2, added_by=self.user, note=8)
        RatingFactory.create(added_by=self.user, note=7)

        note = 8
        queryset = Rating.objects.filter(
            added_by=self.user, note__lt=note
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'note__lt': note})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_note_exact(self):
        RatingFactory.create_batch(2, added_by=self.user, note=8)
        RatingFactory.create(added_by=self.user, note=7)

        note = 7
        queryset = Rating.objects.filter(
            added_by=self.user, note=note
        )

        self._require_login()
        response = self.client.get(self.list_url, {'note': note})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_note_range(self):
        RatingFactory.create(added_by=self.user, note=9)
        RatingFactory.create(added_by=self.user, note=8)
        RatingFactory.create(added_by=self.user, note=7)
        RatingFactory.create(added_by=self.user, note=1)

        note_min, note_max = 7, 9
        queryset = Rating.objects.filter(
            added_by=self.user, note__range=(note_min, note_max)
        ).order_by('-created_at')

        self._require_login()
        response = self.client.get(self.list_url, {'note__range': f'{note_min},{note_max}'})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_is_published(self):
        RatingFactory.create_batch(2, added_by=self.user, is_published=True)
        RatingFactory.create_batch(2, added_by=self.user, is_published=False)

        queryset = Rating.objects.filter(
            added_by=self.user, is_published=True
        )

        self._require_login()
        response = self.client.get(self.list_url, {'is_published': True})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_list_ratings_filter_is_not_published(self):
        RatingFactory.create_batch(2, added_by=self.user, is_published=True)
        RatingFactory.create_batch(2, added_by=self.user, is_published=False)

        queryset = Rating.objects.filter(
            added_by=self.user, is_published=False
        )

        self._require_login()
        response = self.client.get(self.list_url, {'is_published': False})
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json['count'], queryset.count())

    def test_create_rating(self):
        beer = BeerFactory()
        beer_purchase = BeerPurchaseFactory(beer=beer, sold_to=self.user)
        payload = {
            'beer': beer.id,
            'beer_purchase': beer_purchase.id,
            'color': 'Very nice color!',
            'foam': 'Small foam but persistent.',
            'smell': 'Tropical fruit, citrus, mango.',
            'taste': 'Coconut, pineapple, grapefruit, bitterness.',
            'opinion': 'Very nice beer! Would drink again!',
            'note': 7,
        }
        self._require_login()
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = Rating.objects.get(id=response_json['id'])
        self.assertEqual(rating.beer, beer)
        self.assertEqual(rating.beer_purchase, beer_purchase)
        self.assertEqual(rating.added_by, self.user)
        self.assertEqual(rating.room, None)
        self.assertEqual(rating.color, payload['color'])
        self.assertEqual(rating.foam, payload['foam'])
        self.assertEqual(rating.smell, payload['smell'])
        self.assertEqual(rating.taste, payload['taste'])
        self.assertEqual(rating.opinion, payload['opinion'])
        self.assertEqual(rating.note, payload['note'])

    def test_create_rating_empty_fields(self):
        beer = BeerFactory()
        payload = {
            'beer': beer.id,
        }
        self._require_login()
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        rating = Rating.objects.get(id=response_json['id'])
        self.assertEqual(rating.beer, beer)
        self.assertEqual(rating.added_by, self.user)
        self.assertEqual(rating.beer_purchase, None)
        self.assertEqual(rating.room, None)
        self.assertEqual(rating.color, None)
        self.assertEqual(rating.foam, None)
        self.assertEqual(rating.smell, None)
        self.assertEqual(rating.taste, None)
        self.assertEqual(rating.opinion, None)
        self.assertEqual(rating.note, None)

    def test_create_rating_beer_not_exists(self):
        payload = {
            'beer': 1000,
        }
        self._require_login()
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer', response_json)

    def test_create_rating_missing_fields(self):
        payload = {
            'color': 'aaa',
            'foam': 'bbb',
            'smell': 'ccc',
            'taste': 'ddd',
            'opinion': 'eee',
            'note': 7,
        }
        self._require_login()
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('beer', response_json)

    def test_create_rating_invalid_note(self):
        beer = BeerFactory()
        payload = {
            'beer': beer.id,
            'note': 11
        }
        self._require_login()
        response = self.client.post(self.list_url, payload)
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('note', response_json)

    def test_retrieve_rating(self):
        rating = RatingFactory(added_by=self.user)
        self._require_login()
        response = self.client.get(
            reverse_lazy('ratings-detail', args=(rating.id,))
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response_json, RatingDetailSerializer(rating).data)

    def test_retrieve_rating_not_exists(self):
        self._require_login()
        response = self.client.get(
            reverse_lazy('ratings-detail', args=(69,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_retrieve_rating_does_not_belong_to_current_user(self):
        rating = RatingFactory()
        self._require_login()
        response = self.client.get(
            reverse_lazy('ratings-detail', args=(rating.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_update_rating(self):
        rating = RatingFactory(added_by=self.user)
        payload = {
            'color': 'New color!',
            'foam': 'New foam!',
            'smell': 'New smell!',
            'taste': 'New taste!',
            'opinion': 'New opinion!',
            'note': 9,
        }
        self._require_login()
        response = self.client.patch(
            reverse_lazy('ratings-detail', args=(rating.id,)),
            payload
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rating.refresh_from_db()
        self.assertEqual(rating.color, payload['color'])
        self.assertEqual(rating.foam, payload['foam'])
        self.assertEqual(rating.smell, payload['smell'])
        self.assertEqual(rating.taste, payload['taste'])
        self.assertEqual(rating.opinion, payload['opinion'])
        self.assertEqual(rating.note, payload['note'])

    def test_update_rating_read_only_field(self):
        beer = BeerFactory()
        rating = RatingFactory(added_by=self.user)
        payload = {
            'beer': beer.id,
        }
        self._require_login()
        response = self.client.patch(
            reverse_lazy('ratings-detail', args=(rating.id,)),
            payload
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        rating.refresh_from_db()
        self.assertNotEqual(rating.beer, beer)

    def test_update_rating_note_invalid(self):
        rating = RatingFactory(added_by=self.user)
        payload = {
            'note': 11
        }
        self._require_login()
        response = self.client.patch(
            reverse_lazy('ratings-detail', args=(rating.id,)),
            payload
        )
        response_json = response.json()
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('note', response_json)

    def test_delete_rating(self):
        rating = RatingFactory(added_by=self.user)
        self._require_login()
        response = self.client.delete(
            reverse_lazy('ratings-detail', args=(rating.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_delete_rating_not_exists(self):
        self._require_login()
        response = self.client.delete(
            reverse_lazy('ratings-detail', args=(69,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_delete_rating_does_not_belong_to_current_user(self):
        rating = RatingFactory()
        self._require_login()
        response = self.client.delete(
            reverse_lazy('ratings-detail', args=(rating.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn('detail', response.json())

    def test_delete_rating_belongs_to_room(self):
        room = RoomFactory(host=self.user)
        rating = RatingFactory(added_by=self.user, room=room)
        self._require_login()
        response = self.client.delete(
            reverse_lazy('ratings-detail', args=(rating.id,))
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertIn('detail', response.json())

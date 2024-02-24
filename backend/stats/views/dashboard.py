import datetime
from typing import Any, Iterable

from django.db.models import QuerySet, Avg
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from beers.models import Beer, BeerStyle, Brewery
from beers.serializers import (
    SimplifiedBeerSerializer,
    EmbeddedBeerStyleSerializer
)
from beers.serializers.brewery import SimplifiedBrewerySerializer
from ratings.models import Rating
from ratings.serializers.rating import RatingWithSimplifiedBeerSerializer
from rooms.models import Room
from rooms.serializers.room import RoomListSerializer
from stats.serializers.dashboard import (
    StatisticsQueryParamsSerializer,
    DashboardStatisticsSerializer
)
from users.models import User


class DashboardStatisticsAPIView(APIView):
    """
    GET     /api/statistics/dashboard   - returns filtered data to populate the dashboard
    """
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[StatisticsQueryParamsSerializer],
        responses=DashboardStatisticsSerializer
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """
        Collects statistics specific to the current user.

        Query parameters:
            - `date_from*`    - date (YYYY-MM-DD, lesser than date_to)
            - `date_to*`      - date (YYYY-MM-DD)
        """
        serializer = StatisticsQueryParamsSerializer(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data

        date_from: datetime.date = data['date_from']
        date_to: datetime.date = data['date_to']

        users = User.objects.filter(id=request.user.id)

        statistics = get_statistics_for_users(
            users=users,
            date_from=date_from,
            date_to=date_to
        )
        return Response(statistics, status=status.HTTP_200_OK)


def get_statistics_for_users(
    users: QuerySet[User],
    date_from: datetime.date,
    date_to: datetime.date
) -> dict:
    ratings = filter_ratings_for_users(users, date_from, date_to).order_by('-note')
    average_rating = get_average_rating(ratings)

    highest_rating = ratings.first()

    if highest_rating:
        highest_rating = serialize_rating(highest_rating)

    lowest_rating = ratings.last()

    if lowest_rating:
        lowest_rating = serialize_rating(lowest_rating)

    rooms_joined = filter_joined_rooms_for_users(users, date_from, date_to)
    rooms_joined_count = rooms_joined.count()

    rooms_created = filter_created_rooms_for_users(users, date_from, date_to)
    rooms_created_count = rooms_created.count()

    rooms_with_users = filter_current_rooms_for_users(users)
    current_rooms = serialize_rooms(rooms_with_users)

    consumed_beers = filter_consumed_beers_for_users(users, date_from, date_to).order_by('-ratings__note').distinct()
    consumed_beers_count = consumed_beers.count()

    recently_consumed_beers_limit = 5
    recently_consumed_beers = consumed_beers[:recently_consumed_beers_limit]
    recently_consumed_beers = serialize_beers(recently_consumed_beers)

    beer_styles = filter_beer_styles_from_beers(consumed_beers)
    beer_styles_count = beer_styles.count()

    ordered_beer_styles = beer_styles.order_by('-beers__ratings__note')
    favourite_beer_style = ordered_beer_styles.first()

    if favourite_beer_style:
        favourite_beer_style = serialize_beer_style(favourite_beer_style)

    breweries = filter_breweries_from_beers(consumed_beers)
    breweries_count = breweries.count()

    ordered_breweries = breweries.order_by('-beers__ratings__note')
    favourite_brewery = ordered_breweries.first()

    if favourite_brewery:
        favourite_brewery = serialize_brewery(favourite_brewery)

    beer_styles_distribution = get_beer_styles_distribution(beer_styles)
    breweries_distribution = get_breweries_distribution(breweries)

    aggregated_data = {
        'consumed_beers_count': consumed_beers_count,
        'average_rating': average_rating,
        'rooms_joined_count': rooms_joined_count,
        'rooms_created_count': rooms_created_count,
        'current_rooms': current_rooms,
        'recently_consumed_beers': recently_consumed_beers,
        'highest_rating': highest_rating,
        'lowest_rating': lowest_rating,
        'beer_styles_count': beer_styles_count,
        'favourite_beer_style': favourite_beer_style,
        'breweries_count': breweries_count,
        'favourite_brewery': favourite_brewery,
        'beer_styles_distribution_chart': beer_styles_distribution,
        'breweries_distribution_chart': breweries_distribution,
    }

    return aggregated_data


def filter_consumed_beers_for_users(
    users: QuerySet[User],
    date_from: datetime.date,
    date_to: datetime.date
) -> QuerySet[Beer]:
    return Beer.objects.filter(
        ratings__added_by__in=users,
        ratings__created_at__range=(date_from, date_to)
    ).select_related('brewery', 'style')


def filter_ratings_for_users(
    users: QuerySet[User],
    date_from: datetime.date,
    date_to: datetime.date
) -> QuerySet[Rating]:
    return Rating.objects.filter(
        added_by__in=users,
        created_at__range=(date_from, date_to)
    )


def filter_joined_rooms_for_users(
    users: QuerySet[User],
    date_from: datetime.date,
    date_to: datetime.date
) -> QuerySet[Room]:
    return Room.objects.filter(
        ratings__added_by__in=users,
        ratings__created_at__range=(date_from, date_to)
    ).distinct()


def filter_created_rooms_for_users(
    users: QuerySet[User],
    date_from: datetime.date,
    date_to: datetime.date
) -> QuerySet[Room]:
    return Room.objects.filter(
        host__in=users,
        created_at__range=(date_from, date_to)
    ).distinct()


def filter_current_rooms_for_users(users: QuerySet[User]) -> QuerySet[Room]:
    return Room.objects.filter(users__in=users).distinct()


def filter_beer_styles_from_beers(beers: QuerySet[Beer]) -> QuerySet[BeerStyle]:
    styles_ids = beers.values_list('style_id', flat=True)
    return BeerStyle.objects.filter(id__in=styles_ids)


def filter_breweries_from_beers(beers: QuerySet[Beer]) -> QuerySet[Brewery]:
    breweries_ids = beers.values_list('brewery_id', flat=True)
    return Brewery.objects.filter(id__in=breweries_ids)


def get_items_occurrences(items: Iterable[Any]) -> list[tuple[Any, int]]:
    registry = {}

    for item in items:
        registry[item] = registry.get(item, 0) + 1

    return sorted(registry.items(), key=lambda x: x[1], reverse=True)


def get_beer_styles_distribution(beer_styles: QuerySet[BeerStyle]) -> list[dict[str, int]]:
    names = beer_styles.values_list('name', flat=True)
    occurrences = get_items_occurrences(names)
    return [{'name': name, 'count': count} for name, count in occurrences]


def get_breweries_distribution(breweries: QuerySet[Brewery]) -> list[dict[str, int]]:
    names = breweries.values_list('name', flat=True)
    occurrences = get_items_occurrences(names)
    return [{'name': name, 'count': count} for name, count in occurrences]


def get_average_rating(ratings: QuerySet[Rating]) -> float | None:
    average_rating = ratings.aggregate(Avg('note'))['note__avg']
    return round(average_rating, 2) if average_rating else None


def serialize_rating(rating: Rating) -> dict:
    serializer = RatingWithSimplifiedBeerSerializer(rating)
    return serializer.data


def serialize_beers(beers: QuerySet[Beer]) -> list[dict]:
    serializer = SimplifiedBeerSerializer(beers, many=True)
    return serializer.data


def serialize_rooms(rooms: QuerySet[Room]) -> list[dict]:
    serializer = RoomListSerializer(rooms, many=True)
    return serializer.data


def serialize_beer_style(beer_style: BeerStyle) -> dict:
    serializer = EmbeddedBeerStyleSerializer(beer_style)
    return serializer.data


def serialize_brewery(brewery: Brewery) -> dict:
    serializer = SimplifiedBrewerySerializer(brewery)
    return serializer.data

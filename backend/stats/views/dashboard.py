import datetime
from typing import Any

from django.db.models import QuerySet, Avg
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from beers.models import Beer
from ratings.models import Rating
from rooms.models import Room
from rooms.serializers.room import RoomListSerializer
from stats.serializers.dashboard import StatisticsQueryParamsSerializer, DashboardStatisticsSerializer
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
    consumed_beers = Beer.objects.filter(
        ratings__added_by__in=users,
        ratings__created_at__range=(date_from, date_to)
    ).order_by('-ratings__note').select_related('brewery', 'style').distinct()
    consumed_beers_count = consumed_beers.count()

    ratings = Rating.objects.filter(
        added_by__in=users,
        created_at__range=(date_from, date_to)
    ).order_by('-note')

    average_rating = ratings.aggregate(Avg('note'))['note__avg']
    rounded_avg_rating = round(average_rating, 2) if average_rating else None

    # highest_rating = ratings.first()
    # lowest_rating = ratings.last()

    rooms_joined = Room.objects.filter(
        ratings__added_by__in=users,
        ratings__created_at__range=(date_from, date_to)
    ).distinct()
    rooms_joined_count = rooms_joined.count()

    rooms_created = Room.objects.filter(
        host__in=users,
        created_at__range=(date_from, date_to)
    ).distinct()
    rooms_created_count = rooms_created.count()

    # if highest_rating:
    #     highest_rating = RatingWithSimplifiedBeerSerializer(highest_rating).data

    # if lowest_rating:
    #     lowest_rating = RatingWithSimplifiedBeerSerializer(lowest_rating).data

    # recently_consumed_beers = consumed_beers[:5]
    # recently_consumed_beers = SimplifiedBeerSerializer(recently_consumed_beers, many=True).data

    rooms_with_users = Room.objects.filter(users__in=users)
    current_rooms = RoomListSerializer(rooms_with_users, many=True).data

    aggregated_data = {
        'consumed_beers_count': consumed_beers_count,
        'average_rating': rounded_avg_rating,
        'rooms_joined_count': rooms_joined_count,
        'rooms_created_count': rooms_created_count,
        'current_rooms': current_rooms,
        # todo: uncomment when frontend is ready to display this data
        # 'highest_rating': highest_rating,
        # 'lowest_rating': lowest_rating,
        # 'recently_consumed_beers': recently_consumed_beers
    }
    return aggregated_data

from typing import Any

from django.db.models import QuerySet
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from beers.models import Beer
from beers.serializers import BeerSerializer
from rooms.models import Room, BeerInRoom
from rooms.permissions import IsHostOrListOnly
from rooms.serializers.room import RoomAddBeerSerializer, RoomDeleteBeerSerializer
from rooms.views.helpers import check_if_room_exists


class BeersInRoomView(GenericAPIView):
    """
    GET     /api/rooms/<str:name>/beers/                        - Lists all beers in this room

    PUT     /api/rooms/<str:name>/beers/                        - Adds beer with given id to beers in this room

    DELETE  /api/rooms/<str:name>/beers/?beer_id=<int:id>       - Removes beer with given id from this room
    """
    permission_classes = [IsAuthenticated, IsHostOrListOnly]
    lookup_url_kwarg = 'room_name'
    serializer_class = None
    serializer_list_class = BeerSerializer

    def get_queryset(self) -> QuerySet[BeerInRoom]:
        room_name = self.kwargs.get(self.lookup_url_kwarg)
        return BeerInRoom.objects.filter(
            room__name=room_name
        ).select_related('beer').order_by('order')

    def initial(self, request: Request, *args: Any, **kwargs: Any) -> None:
        room_name = self.kwargs.get(self.lookup_url_kwarg)

        if not check_if_room_exists(room_name):
            raise NotFound(
                detail=f'Room with name `{room_name}` does not exist!'
            )

        super().initial(request, *args, **kwargs)

    @extend_schema(
        responses=BeerSerializer(many=True),
    )
    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        beers_in_room = self.get_queryset()
        beers = Beer.objects.filter(
            id__in=beers_in_room.values_list('beer_id', flat=True)
        ).order_by(
            'rooms_through__order'
        )
        return Response(
            self.serializer_list_class(instance=beers, many=True).data,
            status.HTTP_200_OK
        )

    @extend_schema(
        request=RoomAddBeerSerializer,
        responses=BeerSerializer(many=True),
    )
    def put(self, request: Request, room_name: str, **kwargs: Any) -> Response:
        room = Room.objects.get(name=room_name)
        serializer = RoomAddBeerSerializer(
            data=request.data,
            beers_in_room=self.get_queryset(),
            room=room
        )
        serializer.is_valid(raise_exception=True)
        beers = serializer.save()
        return Response(
            self.serializer_list_class(instance=beers, many=True).data,
            status.HTTP_201_CREATED
        )

    @extend_schema(
        parameters=[RoomDeleteBeerSerializer],
        request=RoomDeleteBeerSerializer,
        responses=None,
    )
    def delete(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        serializer = RoomDeleteBeerSerializer(
            data=request.query_params,
            beers_in_room=self.get_queryset(),
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({'message': 'Successfully removed beer from room!'}, status.HTTP_200_OK)

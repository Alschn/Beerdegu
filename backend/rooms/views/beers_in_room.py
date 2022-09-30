from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from beers.models import Beer
from beers.serializers import BeerSerializer
from rooms.models import Room, BeerInRoom
from rooms.permissions import IsHostOrListOnly
from rooms.views.helpers import check_if_room_exists


class BeersInRoomView(APIView):
    """
    GET     api/rooms/<str:name>/beers - Lists all beers in this room
    PUT     api/rooms/<str:name>/beers - Adds beer with given id to beers in this room
    DELETE  api/rooms/<str:name>/beers/?id=<int:id> - Removes beer with given id from this room
    """
    lookup_url_kwarg = 'room_name'
    permission_classes = [IsAuthenticated, IsHostOrListOnly]

    def get_queryset(self) -> QuerySet[BeerInRoom]:
        room_name = self.kwargs.get(self.lookup_url_kwarg)
        return BeerInRoom.objects.filter(room__name=room_name)

    def get(self, request: Request, room_name: str, **kwargs: Any) -> Response:
        if not check_if_room_exists(room_name):
            return Response(
                {'message': 'Room with given name does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )

        qs = Beer.objects.filter(room__name=room_name)
        return Response({
            'room': room_name,
            'beers': BeerSerializer(qs, many=True).data
        }, status.HTTP_200_OK)

    def put(self, request: Request, room_name: str, **kwargs: Any) -> Response:
        if not check_if_room_exists(room_name):
            return Response(
                {'message': 'Room with given name does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )

        beer_id = request.data.get('beer_id')
        if not beer_id:
            return Response({'message': 'Beer id not found in request body!'}, status.HTTP_400_BAD_REQUEST)

        beer_qs = Beer.objects.filter(id=beer_id)
        if not beer_qs.exists():
            return Response({'message': 'Beer with given id does not exist!'}, status.HTTP_404_NOT_FOUND)

        qs = self.get_queryset()
        if qs.filter(beer__id=beer_id).exists():
            return Response({'message': 'Beer with given is already in this room!'}, status.HTTP_400_BAD_REQUEST)

        Room.objects.get(name=room_name).beers.add(*beer_qs)
        qs = Beer.objects.filter(room__name=room_name)
        return Response({
            'room': room_name,
            'beers': BeerSerializer(qs, many=True).data
        }, status.HTTP_201_CREATED)

    def delete(self, request: Request, room_name: str, **kwargs: Any) -> Response:
        if not check_if_room_exists(room_name):
            return Response(
                {'message': 'Room with given name does not exist!'},
                status=status.HTTP_404_NOT_FOUND
            )

        beer_id = request.query_params.get('id')
        if not beer_id:
            return Response({'message': 'Beer id not found in request parameters!'}, status.HTTP_400_BAD_REQUEST)

        qs = self.get_queryset()
        try:
            qs.get(beer__id=beer_id).delete()
            return Response({'message': 'Successfully removed beer from room!'}, status.HTTP_200_OK)
        except ObjectDoesNotExist:
            return Response({'message': 'Beer with given id was not found in this room!'}, status.HTTP_404_NOT_FOUND)

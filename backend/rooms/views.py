from typing import Any

from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from beers.models import Beer
from beers.serializers import BeerSerializer
from rooms.models import Room, BeerInRoom
from rooms.permissions import IsHostOrListCreateOnly, IsHostOrListOnly
from rooms.serializers import (
    RoomSerializer, DetailedRoomSerializer, CreateRoomSerializer
)


class RoomsViewSet(viewsets.ModelViewSet):
    """
    GET     api/rooms/          - list all rooms
    POST    api/rooms/          - create new room
    GET     api/rooms/<str:name>/ - retrieve room
    PUT     api/rooms/<str:name>/ - update room
    PATCH   api/rooms/<str:name>/ - partially update room
    DELETE  api/rooms/<str:name>/ - delete room

    GET     api/rooms/<str:name>/in/    - check if current user is in the room
    PUT     api/rooms/<str:name>/join/  - handle current user join the room
    DELETE  api/rooms/<str:name>/leave  - handle current user room leave the room
    """
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHostOrListCreateOnly]
    lookup_field = 'name'

    def get_queryset(self) -> QuerySet[Room]:
        if self.action in ["user_in", "user_join", "user_leave"]:
            return Room.objects.all().prefetch_related('users')

        elif self.action in ["list_beers", "add_beer", "remove_beer"]:
            return BeerInRoom.objects.filter(room__name=self.kwargs['name'])

        return Room.objects.all().prefetch_related('users', 'beers')

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return DetailedRoomSerializer
        if hasattr(self, 'action') and self.action == 'create':
            return CreateRoomSerializer
        return super().get_serializer_class()

    def create(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        sender = request.user

        not_finished_hosted_rooms = Room.objects.filter(host=sender).exclude(state=Room.State.FINISHED)

        if not_finished_hosted_rooms.exists():
            return Response(
                {'message': 'User is already a host of another room, which is not in FINISHED state!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        serializer = self.get_serializer_class()(data=request.data, context={'request': request})

        if serializer.is_valid():
            self.perform_create(serializer)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_create(self, serializer) -> None:
        serializer.save(host=self.request.user)

    @action(
        detail=True, methods=['GET'], url_path='in',
        permission_classes=[IsAuthenticated]
    )
    def user_in(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """GET api/rooms/<str:name>/in/"""

        room = self.get_object()
        sender = request.user

        if room.users.filter(id=sender.id).exists():
            is_host: bool = room.host and room.host == sender
            return Response(
                {
                    'message': f'{sender.username} is in this room.',
                    'is_host': is_host,
                },
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': 'User is not part of this room!'},
            status=status.HTTP_403_FORBIDDEN
        )

    @action(
        detail=True, methods=['PUT'], url_path='join',
        permission_classes=[IsAuthenticated]
    )
    def user_join(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """PUT api/rooms/<str:name>/join/"""

        room = self.get_object()
        room_name = room.name
        sender = request.user
        password = request.data.get('password')

        if room.password and not password:
            return Response(
                {'message': f'Room {room_name} is protected. No password found in body'},
                status=status.HTTP_400_BAD_REQUEST
            )

        users_in_room = room.users

        if not users_in_room.filter(id=sender.id).exists():
            if users_in_room.count() >= room.slots:
                return Response({'message': f'Room {room_name} is full!'}, status=status.HTTP_403_FORBIDDEN)

            if room.password and room.password != password:
                return Response({'message': 'Invalid password!'}, status=status.HTTP_403_FORBIDDEN)

            users_in_room.add(sender)

            return Response({'message': f'Joined room {room_name}'}, status=status.HTTP_200_OK)

        return Response({'message': 'User is already in this room!'}, status=status.HTTP_200_OK)

    @action(
        detail=True, methods=['DELETE'], url_path='leave',
        permission_classes=[IsAuthenticated]
    )
    def user_leave(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """DELETE api/rooms/<str:name>/leave"""

        room = self.get_object()
        sender = request.user
        users_in_room = room.users

        if users_in_room.filter(id=sender.id).exists():
            users_in_room.remove(sender)
            return Response({'message': f'{sender.username} has left room {room.name}!'}, status=status.HTTP_200_OK)

        return Response({'message': f'{sender.username} is not inside this room!'}, status=status.HTTP_400_BAD_REQUEST)


def check_if_room_exists(room_name: str):
    return Room.objects.filter(name=room_name).exists()


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

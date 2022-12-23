from datetime import datetime
from typing import Any

from django.db.models import QuerySet
from django.http import FileResponse
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.request import Request
from rest_framework.response import Response

from core.shared.pagination import page_number_pagination_factory
from core.shared.renderers import FileOrJSONRenderer
from rooms.models import Room
from rooms.permissions import IsHostOrListCreateOnly
from rooms.reports import generate_excel_report
from rooms.serializers import (
    RoomSerializer,
    DetailedRoomSerializer,
    CreateRoomSerializer
)

RoomsPagination = page_number_pagination_factory(page_size=100)


class RoomsViewSet(
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    mixins.CreateModelMixin,
    viewsets.GenericViewSet,
):
    """
    GET     /api/rooms/                     - list all rooms
    POST    /api/rooms/                     - create new room
    GET     /api/rooms/<str:name>/          - retrieve room

    GET     /api/rooms/<str:name>/in/       - check if current user is in the room
    PUT     /api/rooms/<str:name>/join/     - handle current user join the room
    DELETE  /api/rooms/<str:name>/leave/    - handle current user room leave the room

    GET     /api/rooms/<str:name>/report/   - generate excel report with results of a session
    """
    permission_classes = [IsAuthenticated, IsHostOrListCreateOnly]
    pagination_class = RoomsPagination
    serializer_class = RoomSerializer
    lookup_field = 'name'

    def get_queryset(self) -> QuerySet[Room]:
        if self.action in ["user_in", "user_join", "user_leave"]:
            return Room.objects.order_by('id').prefetch_related('users')

        # elif self.action in ["list_beers", "add_beer", "remove_beer"]:
        #     return BeerInRoom.objects.filter(room__name=self.kwargs['name'])

        return Room.objects.order_by('id').prefetch_related('users', 'beers')

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return DetailedRoomSerializer

        if self.action == 'create':
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

    @action(
        detail=True, methods=['GET'], url_path='report',
        permission_classes=[IsAuthenticated],
        renderer_classes=[FileOrJSONRenderer]
    )
    def download_report(self, request: Request, *args: Any, **kwargs: Any) -> Response | FileResponse:
        """GET api/rooms/<str:name>/report/"""

        room: Room = self.get_object()
        user = self.request.user

        if not room.users.filter(id=user.id).exists():
            return Response(
                {'message': 'User is not part of this room!'},
                status=status.HTTP_403_FORBIDDEN
            )

        if room.state != Room.State.FINISHED:
            return Response(
                {'message': 'Room is not in FINISHED state! Cannot generate report!'},
                status=status.HTTP_400_BAD_REQUEST
            )

        file_buffer = generate_excel_report(room.name, user)

        today = datetime.today().strftime('%d_%m_%Y')
        file_name = f"beerdegu_degustacja_{today}.xlsx"

        response = FileResponse(
            file_buffer,
            content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            status=status.HTTP_200_OK
        )
        response['Content-Length'] = file_buffer.getbuffer().nbytes
        response['Content-Disposition'] = f'attachment; filename="{file_name}"'
        return response

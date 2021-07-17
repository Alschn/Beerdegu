from rest_framework import status, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.models import Room
from rooms.permissions import IsHostOrListCreateOnly
from rooms.serializers import RoomSerializer, DetailedRoomSerializer


class UserIsInRoom(APIView):
    """GET api/rooms/in?code=<str:name>"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender = request.user
        room_code = request.query_params.get('code')

        if not room_code:
            return Response(
                {'message': 'Missing code parameter in query!'},
                status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(name=room_code)
        if not rooms.exists():
            return Response(
                {'message': 'Room with given code not found!'},
                status=status.HTTP_404_NOT_FOUND)

        room = rooms.first()
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


class RoomsViewSet(viewsets.ModelViewSet):
    """
    GET     api/rooms/          - list all rooms
    POST    api/rooms/          - create new room
    GET     api/rooms/<int:id>/ - retrieve room
    PUT     api/rooms/<int:id>/ - update room
    PATCH   api/rooms/<int:id>/ - partially update room
    DELETE  api/rooms/<int:id>/ - delete room
    """
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    permission_classes = [IsAuthenticated, IsHostOrListCreateOnly]

    def get_serializer_class(self):
        if hasattr(self, 'action') and self.action in ['list', 'retrieve']:
            return DetailedRoomSerializer
        return super().get_serializer_class()


class JoinRoom(APIView):
    """PUT api/rooms/<str:name>/join"""

    def put(self, request, room_name):
        room_query = Room.objects.filter(name=room_name)
        sender = request.user

        if not room_query.exists():
            return Response({'message': 'Room not found!'}, status=status.HTTP_404_NOT_FOUND)

        room = room_query.first()
        users_in_room = room.users

        if not users_in_room.filter(id=sender.id).exists():
            if users_in_room.count() >= room.slots:
                return Response({'message': f'Room {room_name} is full!'}, status=status.HTTP_403_FORBIDDEN)

            users_in_room.add(sender)

            return Response({'message': f'Joined room {room_name}'}, status=status.HTTP_200_OK)

        return Response({'message': 'User is already in this room!'}, status=status.HTTP_400_BAD_REQUEST)


class LeaveRoom(APIView):
    """DELETE api/rooms/<str:name>/leave"""

    def delete(self, request, room_name):
        room_query = Room.objects.filter(name=room_name)
        sender = request.user

        if not room_query.exists():
            return Response({'message': 'Room not found!'}, status=status.HTTP_404_NOT_FOUND)

        room = room_query.first()
        users_in_room = room.users

        if users_in_room.filter(id=sender.id).exists():
            users_in_room.remove(sender)
            return Response({'message': f'{sender.username} has left room {room_name}!'}, status=status.HTTP_200_OK)

        return Response({'message': f'{sender.username} is not inside this room!'}, status=status.HTTP_400_BAD_REQUEST)

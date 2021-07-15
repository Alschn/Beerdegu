from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from rooms.models import Room


class UserIsInRoom(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        sender = request.user
        room_code = request.query_params.get('code')

        if not room_code:
            return Response(
                {'message': 'Missing room_code parameter in query!'},
                status=status.HTTP_400_BAD_REQUEST)

        rooms = Room.objects.filter(name=room_code)
        if not rooms.exists():
            return Response(
                {'message': 'Room with given code not found!'},
                status=status.HTTP_404_NOT_FOUND)

        room = rooms.first()
        if room.users.filter(id=sender.id).exists():
            return Response(
                {'message': f'{sender.username} is in this room.'},
                status=status.HTTP_200_OK
            )

        return Response(
            {'message': 'User is not part of this room!'},
            status=status.HTTP_403_FORBIDDEN
        )

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from rooms.models import Room

PROTECTED_METHODS = ['PUT', 'PATCH', 'DELETE']
ALLOWED_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']


class IsHostOrListCreateOnly(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Room) -> bool:
        # safe methods + POST to create a new room
        if request.method in ALLOWED_METHODS:
            return True

        # host condition
        elif request.method in PROTECTED_METHODS and (obj.host and obj.host == request.user):
            return True

        # otherwise permission denied
        return False


class IsHostOrListOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        # list condition
        if request.method == 'GET':
            return True

        room = Room.objects.filter(name=view.kwargs['room_name'])
        room_exists = room.exists()

        # host condition
        if room_exists and room.first().host == request.user:
            return True

        # let view handle 404 instead of permission raising 403
        elif not room_exists:
            return True

        # otherwise, permission denied
        return False

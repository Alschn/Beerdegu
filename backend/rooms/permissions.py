from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request
from rest_framework.views import APIView

from rooms.models import Room

PROTECTED_METHODS = ['PUT', 'PATCH', 'DELETE']
ALLOWED_METHODS = ['GET', 'HEAD', 'OPTIONS', 'POST']


class IsHostOrListCreateOnly(BasePermission):
    def has_object_permission(self, request: Request, view: APIView, obj: Room) -> bool:
        if request.method in PROTECTED_METHODS:
            if obj.host and obj.host == request.user:
                return True
        elif request.method in ALLOWED_METHODS:
            return True
        return False


class IsHostOrListOnly(BasePermission):
    def has_permission(self, request: Request, view: APIView) -> bool:
        if request.method == 'GET':
            return True
        room = Room.objects.filter(name=view.kwargs.get('room_name'))
        if room.exists():
            if room.first().host != request.user:
                return False
        return True

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from ratings.models import Rating
from rooms.models import Room


class CanEditRatingPermission(BasePermission):
    """
    Ratings can be edited and deleted by their authors when:
    - the connected room is in progress
    - rating is not connected to any room
    """
    protected_methods = ('DELETE', 'PATCH', 'PUT')

    def has_object_permission(self, request: Request, view: APIView, obj: Rating) -> bool:
        if request.method.upper() not in self.protected_methods:
            return True

        if obj.room and obj.room != Room.State.IN_PROGRESS:
            return False

        return obj.added_by == request.user

from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from rest_framework.views import APIView

from rooms.models import Rating


class CanDeleteRatingPermission(BasePermission):
    """
    Ratings can be deleted by their authors, only if they are not associated with a room.
    """

    def has_object_permission(self, request: Request, view: APIView, obj: Rating) -> bool:
        if request.method != 'DELETE':
            return True

        return obj.room is None and obj.added_by == request.user

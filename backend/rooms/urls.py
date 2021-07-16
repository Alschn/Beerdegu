from django.urls import path, include
from rest_framework.routers import DefaultRouter

from rooms.views import RoomsViewSet, UserIsInRoom

router = DefaultRouter()
router.register(r'rooms', RoomsViewSet, basename='rooms')

urlpatterns = [
    path('', include(router.urls)),
    path('rooms/in', UserIsInRoom.as_view(), name='user_in_room')

]

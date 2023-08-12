from django.urls import path
from rest_framework.routers import DefaultRouter

from rooms.views import (
    RoomsViewSet,
    BeersInRoomView
)

router = DefaultRouter()
router.register(r'rooms', RoomsViewSet, basename='rooms')

urlpatterns = [
    *router.urls,
    path('rooms/<str:room_name>/beers/', BeersInRoomView.as_view(), name='rooms-detail-beers')
]

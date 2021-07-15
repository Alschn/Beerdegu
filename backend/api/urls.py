from django.urls import path, include

from rooms.views import UserIsInRoom
from .views import SimpleAPIView

urlpatterns = [
    path('test', SimpleAPIView.as_view(), name='test_api_view'),
    path('', include('beers.urls')),

    path('in', UserIsInRoom.as_view(), name='user_in_room')
]

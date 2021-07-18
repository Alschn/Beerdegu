from django.urls import path, include

urlpatterns = [
    path('', include('beers.urls')),
    path('', include('rooms.urls')),
]

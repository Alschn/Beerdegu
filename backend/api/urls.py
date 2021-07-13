from django.urls import path, include

from .views import SimpleAPIView

urlpatterns = [
    path('test', SimpleAPIView.as_view(), name='test_api_view'),
    path('', include('beers.urls')),
]

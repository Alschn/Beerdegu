from django.urls import path

from .views import DashboardStatisticsAPIView

urlpatterns = [
    path('statistics/dashboard/', DashboardStatisticsAPIView.as_view(), name='statistics-dashboard'),
]

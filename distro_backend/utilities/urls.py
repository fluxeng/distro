from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserLocationLoggerView, DashboardStatsView

urlpatterns = [
    path('gps/', UserLocationLoggerView.as_view(), name="gps-log"),
    path('dashboard/', DashboardStatsView.as_view(), name="dashboard-stats"),
]

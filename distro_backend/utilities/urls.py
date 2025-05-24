from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, DashboardStatsView

router = DefaultRouter()
router.register(r'users', UserViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', DashboardStatsView.as_view(), name='dashboard-stats'),
]
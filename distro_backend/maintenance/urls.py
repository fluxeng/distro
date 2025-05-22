from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import IssueViewSet, MaintenanceTaskViewSet  # You'll create these later

router = DefaultRouter()
# router.register(r'issues', IssueViewSet)
# router.register(r'tasks', MaintenanceTaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
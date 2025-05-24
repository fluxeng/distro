from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import IssueViewSet, MaintenanceTaskViewSet, WorkOrderViewSet

router = DefaultRouter()
router.register(r'issues', IssueViewSet)
router.register(r'tasks', MaintenanceTaskViewSet)
router.register(r'work-orders', WorkOrderViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
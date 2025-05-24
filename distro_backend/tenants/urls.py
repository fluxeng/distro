from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UtilityViewSet

router = DefaultRouter()
router.register(r'utilities', UtilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
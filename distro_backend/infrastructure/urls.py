from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    AssetViewSet, PipeViewSet, ValveViewSet,
    MeterViewSet, ZoneViewSet, AssetMapViewSet
)

router = DefaultRouter()
router.register(r'assets', AssetViewSet)
router.register(r'pipes', PipeViewSet)
router.register(r'valves', ValveViewSet)
router.register(r'meters', MeterViewSet)
router.register(r'zones', ZoneViewSet)
router.register(r'asset-map', AssetMapViewSet, basename='asset-map')  # Added unique basename

urlpatterns = [
    path('', include(router.urls)),
]
from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import AssetViewSet, PipeViewSet, ValveViewSet  # You'll create these later

router = DefaultRouter()
# router.register(r'assets', AssetViewSet)
# router.register(r'pipes', PipeViewSet)
# router.register(r'valves', ValveViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
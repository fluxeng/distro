from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import UtilityViewSet  # You'll create this later

router = DefaultRouter()
# router.register(r'profile', UtilityViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
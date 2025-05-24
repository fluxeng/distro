from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tenants'

# Create a router and register our viewsets with it
router = DefaultRouter()
router.register(r'tenants', views.TenantViewSet, basename='tenant')

# The API URLs are now determined automatically by the router
urlpatterns = [
    path('', include(router.urls)),
]

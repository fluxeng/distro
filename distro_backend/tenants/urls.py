# tenants/urls.py
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

app_name = 'tenants'

router = DefaultRouter()
router.register(r'', views.TenantViewSet, basename='tenant')

urlpatterns = [
    path('', include(router.urls)),
]
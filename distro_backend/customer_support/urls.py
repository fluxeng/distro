from django.urls import path, include
from rest_framework.routers import DefaultRouter
# from .views import TicketViewSet, CustomerViewSet  # You'll create these later

router = DefaultRouter()
# router.register(r'tickets', TicketViewSet)
# router.register(r'customers', CustomerViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
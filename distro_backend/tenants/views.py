from rest_framework import viewsets, permissions
from .models import Utility
from .serializers import UtilitySerializer

class UtilityViewSet(viewsets.ModelViewSet):
    queryset = Utility.objects.all()
    serializer_class = UtilitySerializer
    permission_classes = [permissions.IsAdminUser]  # Restrict to superusers
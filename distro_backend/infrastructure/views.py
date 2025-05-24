from rest_framework import viewsets, permissions
from .models import Asset, Pipe, Valve, Meter, Zone
from .serializers import (
    AssetSerializer, PipeSerializer, ValveSerializer,
    MeterSerializer, ZoneSerializer, AssetMapSerializer
)

class AssetViewSet(viewsets.ModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetSerializer
    permission_classes = [permissions.IsAuthenticated]

class PipeViewSet(viewsets.ModelViewSet):
    queryset = Pipe.objects.all()
    serializer_class = PipeSerializer
    permission_classes = [permissions.IsAuthenticated]

class ValveViewSet(viewsets.ModelViewSet):
    queryset = Valve.objects.all()
    serializer_class = ValveSerializer
    permission_classes = [permissions.IsAuthenticated]

class MeterViewSet(viewsets.ModelViewSet):
    queryset = Meter.objects.all()
    serializer_class = MeterSerializer
    permission_classes = [permissions.IsAuthenticated]

class ZoneViewSet(viewsets.ModelViewSet):
    queryset = Zone.objects.all()
    serializer_class = ZoneSerializer
    permission_classes = [permissions.IsAuthenticated]

class AssetMapViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Asset.objects.all()
    serializer_class = AssetMapSerializer
    permission_classes = [permissions.IsAuthenticated]
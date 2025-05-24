from rest_framework import viewsets, permissions
from .models import Issue, MaintenanceTask, WorkOrder
from .serializers import IssueSerializer, MaintenanceTaskSerializer, WorkOrderSerializer

class IssueViewSet(viewsets.ModelViewSet):
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer
    permission_classes = [permissions.IsAuthenticated]

class MaintenanceTaskViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceTask.objects.all()
    serializer_class = MaintenanceTaskSerializer
    permission_classes = [permissions.IsAuthenticated]

class WorkOrderViewSet(viewsets.ModelViewSet):
    queryset = WorkOrder.objects.all()
    serializer_class = WorkOrderSerializer
    permission_classes = [permissions.IsAuthenticated]
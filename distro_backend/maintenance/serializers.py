from rest_framework import serializers
from .models import Issue, MaintenanceTask, WorkOrder
from infrastructure.serializers import AssetSerializer

class IssueSerializer(serializers.ModelSerializer):
    asset_details = AssetSerializer(source='affected_asset', read_only=True)
    reported_by_name = serializers.CharField(source='reported_by.get_full_name', read_only=True)

    class Meta:
        model = Issue
        fields = '__all__'
        read_only_fields = ['reported_at', 'updated_at', 'issue_id']

class MaintenanceTaskSerializer(serializers.ModelSerializer):
    assigned_to_name = serializers.CharField(source='assigned_to.get_full_name', read_only=True)

    class Meta:
        model = MaintenanceTask
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'task_id']

class WorkOrderSerializer(serializers.ModelSerializer):
    supervisor_name = serializers.CharField(source='supervisor.get_full_name', read_only=True)

    class Meta:
        model = WorkOrder
        fields = '__all__'
        read_only_fields = ['created_at', 'updated_at', 'order_number']
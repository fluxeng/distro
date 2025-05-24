from rest_framework import serializers
from .models import User, Department, Team
from rest_framework_gis.serializers import GeoFeatureModelSerializer

class UserSerializer(GeoFeatureModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    
    class Meta:
        model = User
        geo_field = 'current_location'
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name',
            'phone_number', 'role', 'department', 'department_name',
            'profile_picture', 'is_field_agent', 'current_location',
            'location_updated_at', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class DepartmentSerializer(serializers.ModelSerializer):
    manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
    
    class Meta:
        model = Department
        fields = [
            'id', 'name', 'description', 'manager',
            'manager_name', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class TeamSerializer(GeoFeatureModelSerializer):
    department_name = serializers.CharField(source='department.name', read_only=True)
    supervisor_name = serializers.CharField(source='supervisor.get_full_name', read_only=True)
    member_count = serializers.IntegerField(source='members.count', read_only=True)
    
    class Meta:
        model = Team
        geo_field = 'coverage_area'
        fields = [
            'id', 'name', 'department', 'department_name',
            'supervisor', 'supervisor_name', 'members',
            'member_count', 'coverage_area', 'created_at',
            'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
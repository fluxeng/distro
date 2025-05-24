from rest_framework import serializers
from rest_framework_gis.serializers import GeoFeatureModelSerializer
from .models import (
    AssetType, Asset, Pipe, Valve, Meter, Zone,
    AssetDocument, AssetPhoto
)

class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = '__all__'

class AssetDocumentSerializer(serializers.ModelSerializer):
    uploaded_by_name = serializers.CharField(source='uploaded_by.get_full_name', read_only=True)
    
    class Meta:
        model = AssetDocument
        fields = [
            'id', 'asset', 'document_type', 'title', 'file',
            'uploaded_by', 'uploaded_by_name', 'uploaded_at'
        ]
        read_only_fields = ['uploaded_at']

class AssetPhotoSerializer(serializers.ModelSerializer):
    taken_by_name = serializers.CharField(source='taken_by.get_full_name', read_only=True)
    
    class Meta:
        model = AssetPhoto
        fields = [
            'id', 'asset', 'image', 'caption', 'taken_by',
            'taken_by_name', 'taken_at'
        ]
        read_only_fields = ['taken_at']

class AssetSerializer(GeoFeatureModelSerializer):
    asset_type_name = serializers.CharField(source='asset_type.name', read_only=True)
    created_by_name = serializers.CharField(source='created_by.get_full_name', read_only=True)
    documents_count = serializers.IntegerField(source='documents.count', read_only=True)
    photos_count = serializers.IntegerField(source='photos.count', read_only=True)
    
    class Meta:
        model = Asset
        geo_field = 'location'
        fields = [
            'id', 'asset_id', 'name', 'asset_type', 'asset_type_name',
            'location', 'address', 'status', 'condition_score',
            'installation_date', 'expected_lifespan', 'warranty_expiry',
            'last_inspection_date', 'next_maintenance_date',
            'manufacturer', 'model_number', 'serial_number',
            'specifications', 'primary_image', 'qr_code',
            'created_by', 'created_by_name', 'documents_count',
            'photos_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class PipeSerializer(GeoFeatureModelSerializer):
    length_km = serializers.SerializerMethodField()
    
    class Meta:
        model = Pipe
        geo_field = 'geometry'
        fields = [
            'id', 'pipe_id', 'geometry', 'length', 'length_km',
            'diameter', 'material', 'pressure_rating',
            'start_node', 'end_node', 'is_active',
            'installation_date', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']
    
    def get_length_km(self, obj):
        return round(obj.length / 1000, 2)

class ValveSerializer(serializers.ModelSerializer):
    asset_details = AssetSerializer(source='asset', read_only=True)
    operated_by_name = serializers.CharField(source='operated_by.get_full_name', read_only=True)
    
    class Meta:
        model = Valve
        fields = [
            'id', 'valve_id', 'asset', 'asset_details', 'valve_type',
            'size', 'current_status', 'last_operation_date',
            'operated_by', 'operated_by_name', 'is_remotely_controlled',
            'control_id'
        ]

class MeterSerializer(serializers.ModelSerializer):
    asset_details = AssetSerializer(source='asset', read_only=True)
    
    class Meta:
        model = Meter
        fields = [
            'id', 'meter_id', 'asset', 'asset_details', 'meter_type',
            'size', 'customer_account', 'last_reading',
            'last_reading_date', 'total_consumption',
            'is_smart_meter', 'communication_id'
        ]

class ZoneSerializer(GeoFeatureModelSerializer):
    inlet_meters_count = serializers.IntegerField(source='inlet_meters.count', read_only=True)
    
    class Meta:
        model = Zone
        geo_field = 'boundary'
        fields = [
            'id', 'name', 'code', 'zone_type', 'boundary',
            'population_served', 'connections', 'inlet_meters',
            'inlet_meters_count', 'created_at', 'updated_at'
        ]
        read_only_fields = ['created_at', 'updated_at']

class AssetMapSerializer(GeoFeatureModelSerializer):
    """Simplified serializer for map display"""
    type_name = serializers.CharField(source='asset_type.name', read_only=True)
    type_icon = serializers.CharField(source='asset_type.icon', read_only=True)
    type_color = serializers.CharField(source='asset_type.color', read_only=True)
    
    class Meta:
        model = Asset
        geo_field = 'location'
        fields = [
            'id', 'asset_id', 'name', 'type_name', 'type_icon',
            'type_color', 'status', 'location'
        ]
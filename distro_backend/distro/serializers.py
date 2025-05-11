from rest_framework import serializers
from .models import UserProfile, AssetType, Asset, Issue, IssueImage

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['id', 'username', 'email', 'role', 'phone_number', 'is_active', 'is_staff']

class AssetTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AssetType
        fields = ['id', 'name', 'description']

class AssetSerializer(serializers.ModelSerializer):
    asset_type = AssetTypeSerializer(read_only=True)
    asset_type_id = serializers.PrimaryKeyRelatedField(
        queryset=AssetType.objects.all(), source='asset_type', write_only=True
    )

    class Meta:
        model = Asset
        fields = ['id', 'name', 'asset_type', 'asset_type_id', 'geometry', 'metadata', 'created_at', 'updated_at']

class IssueImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = IssueImage
        fields = ['id', 'issue', 'image', 'uploaded_at']

class IssueSerializer(serializers.ModelSerializer):
    reported_by = UserProfileSerializer(read_only=True)
    reported_by_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), source='reported_by', write_only=True
    )
    assigned_to = UserProfileSerializer(read_only=True)
    assigned_to_id = serializers.PrimaryKeyRelatedField(
        queryset=UserProfile.objects.all(), source='assigned_to', write_only=True, allow_null=True
    )
    images = IssueImageSerializer(many=True, read_only=True)

    class Meta:
        model = Issue
        fields = [
            'id', 'title', 'description', 'priority', 'status', 'location',
            'reported_by', 'reported_by_id', 'assigned_to', 'assigned_to_id',
            'reported_date', 'updated_date', 'images'
        ]
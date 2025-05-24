from rest_framework import serializers
from .models import Utility, Domain

class UtilitySerializer(serializers.ModelSerializer):
    class Meta:
        model = Utility
        fields = ['id', 'name', 'description', 'contact_email', 'contact_phone', 'address', 'is_active']
        read_only_fields = ['created_on', 'updated_on']

class DomainSerializer(serializers.ModelSerializer):
    class Meta:
        model = Domain
        fields = '__all__'
from django.contrib import admin
from .models import AssetType, Asset, Pipe, Valve, Meter, Zone, AssetDocument, AssetPhoto

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'code']
    search_fields = ['name', 'code']

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ['asset_id', 'name', 'asset_type', 'status']
    search_fields = ['asset_id', 'name']
    list_filter = ['asset_type', 'status']

@admin.register(Pipe)
class PipeAdmin(admin.ModelAdmin):
    list_display = ['pipe_id', 'material', 'diameter', 'is_active']
    search_fields = ['pipe_id']
    list_filter = ['material', 'is_active']

@admin.register(Valve)
class ValveAdmin(admin.ModelAdmin):
    list_display = ['valve_id', 'valve_type', 'current_status']
    search_fields = ['valve_id']
    list_filter = ['valve_type', 'current_status']

@admin.register(Meter)
class MeterAdmin(admin.ModelAdmin):
    list_display = ['meter_id', 'meter_type', 'is_smart_meter']
    search_fields = ['meter_id']
    list_filter = ['meter_type', 'is_smart_meter']

@admin.register(Zone)
class ZoneAdmin(admin.ModelAdmin):
    list_display = ['name', 'code', 'zone_type']
    search_fields = ['name', 'code']
    list_filter = ['zone_type']

@admin.register(AssetDocument)
class AssetDocumentAdmin(admin.ModelAdmin):
    list_display = ['title', 'asset', 'document_type']
    search_fields = ['title']
    list_filter = ['document_type']

@admin.register(AssetPhoto)
class AssetPhotoAdmin(admin.ModelAdmin):
    list_display = ['asset', 'caption', 'taken_at']
    search_fields = ['caption']
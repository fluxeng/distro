from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.gis.db import models as gis_models
from django.utils.html import format_html
from django.http import HttpResponse
import csv
from .models import UserProfile, AssetType, Asset, Issue, IssueImage
from leaflet.admin import LeafletGeoAdminMixin
from django_ckeditor_5.widgets import CKEditor5Widget

class IssueImageInline(admin.TabularInline):
    model = IssueImage
    extra = 1
    fields = ('image', 'uploaded_at', 'image_preview')
    readonly_fields = ('uploaded_at', 'image_preview')

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="100" height="100" />', obj.image.url)
        return "No Image"
    image_preview.short_description = 'Preview'

class GeometryTypeFilter(admin.SimpleListFilter):
    title = 'geometry type'
    parameter_name = 'geometry_type'

    def lookups(self, request, model_admin):
        return (
            ('Point', 'Point'),
            ('LineString', 'LineString'),
        )

    def queryset(self, request, queryset):
        if self.value():
            return queryset.filter(geometry__geom_type=self.value())
        return queryset

class ReportedDateRangeFilter(admin.SimpleListFilter):
    title = 'reported date range'
    parameter_name = 'reported_date_range'

    def lookups(self, request, model_admin):
        return (
            ('last_7_days', 'Last 7 Days'),
            ('last_30_days', 'Last 30 Days'),
            ('older', 'Older than 30 Days'),
        )

    def queryset(self, request, queryset):
        from django.utils import timezone
        from datetime import timedelta
        now = timezone.now()
        if self.value() == 'last_7_days':
            return queryset.filter(reported_date__gte=now - timedelta(days=7))
        elif self.value() == 'last_30_days':
            return queryset.filter(reported_date__gte=now - timedelta(days=30))
        elif self.value() == 'older':
            return queryset.filter(reported_date__lt=now - timedelta(days=30))
        return queryset

def export_as_csv(modeladmin, request, queryset):
    model_name = modeladmin.model._meta.model_name
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = f'attachment; filename="{model_name}_export.csv"'
    writer = csv.writer(response)
    
    fields = [f.name for f in modeladmin.model._meta.fields if not isinstance(f, gis_models.GeometryField)]
    writer.writerow(fields)
    
    for obj in queryset:
        row = [str(getattr(obj, field)) for field in fields]
        writer.writerow(row)
    
    return response
export_as_csv.short_description = "Export selected as CSV"

@admin.register(UserProfile)
class UserProfileAdmin(UserAdmin):
    model = UserProfile
    list_display = ('username', 'email', 'role', 'phone_number', 'is_staff', 'is_active')
    list_filter = ('role', 'is_staff', 'is_active')
    search_fields = ('username', 'email', 'phone_number')
    ordering = ('username',)
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal Info', {'fields': ('first_name', 'last_name', 'email', 'role', 'phone_number', 'push_token')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'email', 'role', 'phone_number', 'password1', 'password2'),
        }),
    )
    def get_fields(self, request, obj=None):
        fields = super().get_fields(request, obj)
        if not request.user.is_superuser:
            fields.remove('push_token')
        return fields

@admin.register(AssetType)
class AssetTypeAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')
    search_fields = ('name', 'description')
    list_filter = ('name',)
    ordering = ('name',)
    actions = [export_as_csv]

@admin.register(Asset)
class AssetAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('name', 'asset_type', 'metadata_summary', 'geometry_type', 'created_at')
    list_filter = ('asset_type', 'created_at', GeometryTypeFilter)
    search_fields = ('name', 'asset_type__name')
    readonly_fields = ('created_at', 'updated_at', 'geometry_type')
    fieldsets = (
        (None, {'fields': ('name', 'asset_type')}),
        ('Geometry', {'fields': ('geometry', 'geometry_type')}),
        ('Metadata', {'fields': ('metadata',)}),
        ('Timestamps', {'fields': ('created_at', 'updated_at')}),
    )
    ordering = ('name',)
    actions = [export_as_csv]
    autocomplete_fields = ['asset_type']
    
    def metadata_summary(self, obj):
        return ', '.join(f"{k}: {v}" for k, v in obj.metadata.items() if k in ['diameter', 'material', 'type', 'reading', 'capacity'])
    metadata_summary.short_description = 'Metadata'

    def geometry_type(self, obj):
        return obj.geometry.geom_type
    geometry_type.short_description = 'Geometry Type'

@admin.register(Issue)
class IssueAdmin(LeafletGeoAdminMixin, admin.ModelAdmin):
    list_display = ('title', 'priority', 'status', 'reported_by', 'assigned_to', 'image_count', 'reported_date')
    list_filter = ('priority', 'status', 'reported_date', ReportedDateRangeFilter)
    search_fields = ('title', 'description', 'reported_by__username', 'assigned_to__username')
    readonly_fields = ('reported_date', 'updated_date', 'image_count')
    fieldsets = (
        (None, {'fields': ('title', 'description', 'priority', 'status')}),
        ('Location', {'fields': ('location',)}),
        ('Assignments', {'fields': ('reported_by', 'assigned_to')}),
        ('Timestamps', {'fields': ('reported_date', 'updated_date')}),
    )
    inlines = [IssueImageInline]
    ordering = ('-reported_date',)
    actions = [export_as_csv, 'mark_as_resolved']
    autocomplete_fields = ['reported_by', 'assigned_to']
    formfield_overrides = {
        gis_models.TextField: {'widget': CKEditor5Widget(config_name='default')},
    }
    
    def image_count(self, obj):
        return obj.images.count()
    image_count.short_description = 'Images'

    def mark_as_resolved(self, request, queryset):
        queryset.update(status='RESOLVED')
        self.message_user(request, "Selected issues marked as resolved.")
    mark_as_resolved.short_description = "Mark selected issues as resolved"

@admin.register(IssueImage)
class IssueImageAdmin(admin.ModelAdmin):
    list_display = ('issue', 'image_thumbnail', 'uploaded_at')
    list_filter = ('uploaded_at',)
    search_fields = ('issue__title',)
    readonly_fields = ('uploaded_at', 'image_thumbnail')
    fieldsets = (
        (None, {'fields': ('issue', 'image', 'image_thumbnail')}),
        ('Timestamps', {'fields': ('uploaded_at',)}),
    )
    ordering = ('-uploaded_at',)
    actions = [export_as_csv]
    
    def image_thumbnail(self, obj):
        if obj.image:
            return format_html('<img src="{}" width="50" height="50" />', obj.image.url)
        return "No Image"
    image_thumbnail.short_description = 'Thumbnail'

admin.site.index_title = "Distro Admin"
admin.site.site_header = "Distro Water Distribution Management"
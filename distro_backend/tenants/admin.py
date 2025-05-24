from django.contrib import admin
from django.db import connection
from django_tenants.admin import TenantAdminMixin
from django_tenants.utils import get_tenant_model, get_public_schema_name

from .models import Utility, Domain


class PublicSchemaOnlyAdmin:
    """
    Base class for admin models that should only be visible in public schema
    """
    def _is_public_schema(self):
        """Check if we're currently in the public schema"""
        try:
            current_schema = connection.schema_name
            public_schema = get_public_schema_name()
            return current_schema == public_schema
        except:
            # Fallback check
            return connection.schema_name in ['public', None]
    
    def has_module_permission(self, request):
        """Only show this admin module in public schema"""
        return self._is_public_schema()
    
    def has_view_permission(self, request, obj=None):
        """Only allow viewing in public schema"""
        return self._is_public_schema()
    
    def has_add_permission(self, request):
        """Only allow adding in public schema"""
        return self._is_public_schema()
    
    def has_change_permission(self, request, obj=None):
        """Only allow changing in public schema"""
        return self._is_public_schema()
    
    def has_delete_permission(self, request, obj=None):
        """Only allow deleting in public schema"""
        return self._is_public_schema()


# Conditionally register admin classes
current_schema = getattr(connection, 'schema_name', 'public')
public_schema = get_public_schema_name()

# Only register these if we're in public schema
if current_schema == public_schema:
    
    @admin.register(Utility)
    class UtilityAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('name', 'schema_name', 'is_active', 'created_on')
        list_filter = ('is_active', 'created_on')
        search_fields = ('name', 'schema_name')
        readonly_fields = ('created_on',)
        
        fieldsets = (
            ('Basic Information', {
                'fields': ('name', 'schema_name')
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
            ('Metadata', {
                'fields': ('created_on',),
                'classes': ('collapse',)
            }),
        )

    @admin.register(Domain)
    class DomainAdmin(TenantAdminMixin, admin.ModelAdmin):
        list_display = ('domain', 'tenant', 'is_primary', 'is_active')
        list_filter = ('is_primary', 'is_active')
        search_fields = ('domain', 'tenant__name')
        
        fieldsets = (
            ('Domain Information', {
                'fields': ('domain', 'tenant', 'is_primary')
            }),
            ('Status', {
                'fields': ('is_active',)
            }),
        )
        
        def get_queryset(self, request):
            qs = super().get_queryset(request)
            return qs.select_related('tenant')

else:
    # In tenant schema - don't register these models at all
    pass
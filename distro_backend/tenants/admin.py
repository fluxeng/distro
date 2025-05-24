from django.contrib import admin
from .models import Utility, Domain

@admin.register(Utility)
class UtilityAdmin(admin.ModelAdmin):
    list_display = ['name', 'schema_name', 'is_active']
    search_fields = ['name', 'schema_name']
    list_filter = ['is_active', 'subscription_tier']

@admin.register(Domain)
class DomainAdmin(admin.ModelAdmin):
    list_display = ['domain', 'tenant']
    search_fields = ['domain']
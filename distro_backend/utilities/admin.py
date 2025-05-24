from django.contrib import admin
from .models import User, Department, Team

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'is_active', 'is_field_agent']
    search_fields = ['username', 'email']
    list_filter = ['is_active', 'is_field_agent']

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ['name', 'manager']
    search_fields = ['name']
    list_filter = ['manager']

@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ['name', 'department', 'supervisor']
    search_fields = ['name']
    list_filter = ['department']
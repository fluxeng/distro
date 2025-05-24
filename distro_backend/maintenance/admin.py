from django.contrib import admin
from .models import Issue, IssuePhoto, MaintenanceLog, MaintenanceTask, WorkOrder

@admin.register(Issue)
class IssueAdmin(admin.ModelAdmin):
    list_display = ['issue_id', 'status', 'priority', 'issue_type', 'reported_at']
    search_fields = ['issue_id', 'description']
    list_filter = ['status', 'priority', 'issue_type']

@admin.register(IssuePhoto)
class IssuePhotoAdmin(admin.ModelAdmin):
    list_display = ['issue', 'uploaded_by', 'uploaded_at']
    search_fields = ['issue__issue_id']
    list_filter = ['uploaded_at']

@admin.register(MaintenanceLog)
class MaintenanceLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'created_by', 'created_at']
    search_fields = ['description', 'log_type']
    list_filter = ['log_type', 'created_at']

@admin.register(MaintenanceTask)
class MaintenanceTaskAdmin(admin.ModelAdmin):
    list_display = ['task_id', 'status', 'scheduled_date', 'created_by']
    search_fields = ['task_id', 'description']
    list_filter = ['status', 'scheduled_date']

@admin.register(WorkOrder)
class WorkOrderAdmin(admin.ModelAdmin):
    list_display = ['work_order_id', 'status', 'created_by', 'created_at']
    search_fields = ['work_order_id', 'description']
    list_filter = ['status', 'created_at']
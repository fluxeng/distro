from django.contrib import admin
from .models import Customer, Ticket, TicketComment, CustomerNotification, ServiceOutage

@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ['account_number', 'name', 'customer_type', 'is_active']
    search_fields = ['account_number', 'name']
    list_filter = ['customer_type', 'is_active']

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ['ticket_number', 'title', 'status', 'priority', 'customer']
    search_fields = ['ticket_number', 'title']
    list_filter = ['status', 'priority', 'ticket_type']

@admin.register(TicketComment)
class TicketCommentAdmin(admin.ModelAdmin):
    list_display = ['ticket', 'created_by', 'created_at', 'is_customer_visible']
    list_filter = ['is_customer_visible']

@admin.register(CustomerNotification)
class CustomerNotificationAdmin(admin.ModelAdmin):
    list_display = ['notification_type', 'channel', 'status', 'customer']
    list_filter = ['notification_type', 'channel', 'status']

@admin.register(ServiceOutage)
class ServiceOutageAdmin(admin.ModelAdmin):
    list_display = ['title', 'outage_type', 'start_time', 'is_active']
    list_filter = ['outage_type', 'is_active']
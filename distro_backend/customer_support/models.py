# customer_support/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from utilities.models import User
from infrastructure.models import Zone, Meter


class Customer(models.Model):
    """Customer accounts"""
    
    CUSTOMER_TYPE_CHOICES = [
        ('residential', 'Residential'),
        ('commercial', 'Commercial'),
        ('industrial', 'Industrial'),
        ('institutional', 'Institutional'),
    ]
    
    # Account information
    account_number = models.CharField(max_length=50, unique=True)
    customer_type = models.CharField(max_length=20, choices=CUSTOMER_TYPE_CHOICES, default='residential')
    
    # Personal/Business information
    name = models.CharField(max_length=200)
    phone_primary = models.CharField(max_length=15)
    phone_secondary = models.CharField(max_length=15, blank=True)
    email = models.EmailField(blank=True)
    
    # Service location
    service_address = models.TextField()
    service_location = gis_models.PointField(null=True, blank=True)
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='customers')
    
    # Meter connection
    meter = models.ForeignKey(Meter, on_delete=models.SET_NULL, null=True, blank=True, related_name='customer_connection')
    
    # Account status
    is_active = models.BooleanField(default=True)
    connection_date = models.DateField(null=True, blank=True)
    disconnection_date = models.DateField(null=True, blank=True)
    
    # Communication preferences
    preferred_language = models.CharField(max_length=10, default='en')
    sms_notifications = models.BooleanField(default=True)
    email_notifications = models.BooleanField(default=False)
    
    # Metadata
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'customers'
        indexes = [
            models.Index(fields=['account_number']),
            models.Index(fields=['phone_primary']),
        ]
    
    def __str__(self):
        return f"{self.account_number} - {self.name}"


class Ticket(models.Model):
    """Customer support tickets"""
    
    TICKET_TYPE_CHOICES = [
        ('complaint', 'Complaint'),
        ('request', 'Service Request'),
        ('inquiry', 'Inquiry'),
        ('report', 'Issue Report'),
        ('billing', 'Billing Issue'),
    ]
    
    CATEGORY_CHOICES = [
        ('no_water', 'No Water Supply'),
        ('low_pressure', 'Low Pressure'),
        ('leak', 'Leak/Burst'),
        ('quality', 'Water Quality'),
        ('billing', 'Billing'),
        ('new_connection', 'New Connection'),
        ('disconnection', 'Disconnection'),
        ('meter', 'Meter Issue'),
        ('other', 'Other'),
    ]
    
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('pending_customer', 'Pending Customer'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    SOURCE_CHOICES = [
        ('phone', 'Phone Call'),
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('web', 'Web Portal'),
        ('mobile_app', 'Mobile App'),
        ('walk_in', 'Walk-in'),
        ('social_media', 'Social Media'),
        ('ussd', 'USSD'),
    ]
    
    # Identification
    ticket_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Classification
    ticket_type = models.CharField(max_length=20, choices=TICKET_TYPE_CHOICES)
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    
    # Customer information
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='tickets')
    reporter_name = models.CharField(max_length=200)
    reporter_phone = models.CharField(max_length=15)
    reporter_email = models.EmailField(blank=True)
    
    # Location (for issue reports)
    issue_location = gis_models.PointField(null=True, blank=True)
    issue_address = models.TextField(blank=True)
    
    # Source tracking
    source = models.CharField(max_length=20, choices=SOURCE_CHOICES)
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_tickets')
    assigned_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_tickets')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Customer satisfaction
    satisfaction_rating = models.IntegerField(null=True, blank=True, choices=[(i, i) for i in range(1, 6)])
    satisfaction_comment = models.TextField(blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tickets')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # SLA tracking
    sla_deadline = models.DateTimeField(null=True, blank=True)
    is_sla_breached = models.BooleanField(default=False)
    
    class Meta:
        db_table = 'tickets'
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['ticket_number']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['customer']),
        ]
    
    def __str__(self):
        return f"{self.ticket_number} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.ticket_number:
            # Generate ticket number
            from datetime import datetime
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.ticket_number = f"TKT-{timestamp}"
        
        # Set SLA deadline based on priority
        if not self.sla_deadline and self.created_at:
            from datetime import timedelta
            sla_hours = {
                'critical': 4,
                'high': 8,
                'medium': 24,
                'low': 48,
            }
            hours = sla_hours.get(self.priority, 24)
            self.sla_deadline = self.created_at + timedelta(hours=hours)
        
        super().save(*args, **kwargs)


class TicketComment(models.Model):
    """Comments on tickets"""
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE, related_name='comments')
    comment = models.TextField()
    
    # Comment type
    is_internal = models.BooleanField(default=False)
    is_customer_visible = models.BooleanField(default=True)
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'ticket_comments'
        ordering = ['created_at']
    
    def __str__(self):
        return f"Comment on {self.ticket.ticket_number}"


class CustomerNotification(models.Model):
    """Notifications sent to customers"""
    
    NOTIFICATION_TYPE_CHOICES = [
        ('outage', 'Service Outage'),
        ('maintenance', 'Planned Maintenance'),
        ('restoration', 'Service Restoration'),
        ('ticket_update', 'Ticket Update'),
        ('general', 'General Information'),
    ]
    
    CHANNEL_CHOICES = [
        ('sms', 'SMS'),
        ('email', 'Email'),
        ('push', 'Push Notification'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('sent', 'Sent'),
        ('delivered', 'Delivered'),
        ('failed', 'Failed'),
    ]
    
    # Notification details
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPE_CHOICES)
    channel = models.CharField(max_length=20, choices=CHANNEL_CHOICES)
    
    # Recipients
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, help_text="For zone-wide notifications")
    
    # Content
    subject = models.CharField(max_length=200)
    message = models.TextField()
    
    # Related entities
    ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name='notifications')
    
    # Status tracking
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    sent_at = models.DateTimeField(null=True, blank=True)
    delivered_at = models.DateTimeField(null=True, blank=True)
    
    # Error tracking
    error_message = models.TextField(blank=True)
    retry_count = models.IntegerField(default=0)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'customer_notifications'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.get_notification_type_display()} - {self.get_channel_display()}"


class ServiceOutage(models.Model):
    """Planned or unplanned service outages"""
    
    OUTAGE_TYPE_CHOICES = [
        ('planned', 'Planned'),
        ('unplanned', 'Unplanned'),
    ]
    
    # Outage details
    outage_type = models.CharField(max_length=20, choices=OUTAGE_TYPE_CHOICES)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Affected areas
    affected_zones = models.ManyToManyField(Zone, related_name='outages')
    affected_area = gis_models.PolygonField(null=True, blank=True)
    estimated_customers_affected = models.IntegerField(default=0)
    
    # Timeline
    start_time = models.DateTimeField()
    estimated_end_time = models.DateTimeField()
    actual_end_time = models.DateTimeField(null=True, blank=True)
    
    # Status
    is_active = models.BooleanField(default=True)
    
    # Related maintenance work
    related_work_order = models.ForeignKey('maintenance.WorkOrder', on_delete=models.SET_NULL, null=True, blank=True)
    
    # Communication
    notification_sent = models.BooleanField(default=False)
    notification_sent_at = models.DateTimeField(null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'service_outages'
        ordering = ['-start_time']
    
    def __str__(self):
        return f"{self.get_outage_type_display()} Outage - {self.title}"
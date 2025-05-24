# utilities/models.py
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator, MaxValueValidator


class User(AbstractUser):
    """Custom user model with role-based access control"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('supervisor', 'Supervisor'),
        ('technician', 'Field Technician'),
        ('customer_service', 'Customer Service'),
        ('viewer', 'Viewer'),
    ]
    
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='viewer')
    phone_number = models.CharField(max_length=15, blank=True)
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    
    # Location tracking for field agents
    last_location = gis_models.PointField(null=True, blank=True)
    last_location_update = models.DateTimeField(null=True, blank=True)
    
    # Profile
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_field_agent = models.BooleanField(default=False)
    
    # Notifications
    enable_sms_notifications = models.BooleanField(default=True)
    enable_email_notifications = models.BooleanField(default=True)
    enable_push_notifications = models.BooleanField(default=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return f"{self.issue_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.issue_id:
            # Generate issue ID
            from datetime import datetime
            prefix = self.issue_type.upper()[:3]
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.issue_id = f"{prefix}-{timestamp}"
        super().save(*args, **kwargs)


class MaintenanceTask(models.Model):
    """Scheduled or reactive maintenance tasks"""
    
    TASK_TYPE_CHOICES = [
        ('preventive', 'Preventive Maintenance'),
        ('reactive', 'Reactive Maintenance'),
        ('inspection', 'Inspection'),
        ('replacement', 'Replacement'),
        ('upgrade', 'Upgrade'),
    ]
    
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
        ('overdue', 'Overdue'),
    ]
    
    # Identification
    task_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Classification
    task_type = models.CharField(max_length=20, choices=TASK_TYPE_CHOICES)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    
    # Related entities
    asset = models.ForeignKey('infrastructure.Asset', on_delete=models.CASCADE, related_name='maintenance_tasks', null=True, blank=True)
    issue = models.ForeignKey('infrastructure.Issue', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_tasks')
    assigned_team = models.ForeignKey('infrastructure.Team', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    
    # Scheduling
    scheduled_date = models.DateTimeField()
    estimated_duration = models.DurationField()
    
    # Execution
    started_at = models.DateTimeField(null=True, blank=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Work details
    work_performed = models.TextField(blank=True)
    materials_used = models.JSONField(default=list, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_tasks')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'maintenance_tasks'
        ordering = ['scheduled_date']
    
    def __str__(self):
        return f"{self.task_id} - {self.title}"
    
    def save(self, *args, **kwargs):
        if not self.task_id:
            # Generate task ID
            from datetime import datetime
            prefix = 'MT'
            timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
            self.task_id = f"{prefix}-{timestamp}"
        super().save(*args, **kwargs)


class WorkOrder(models.Model):
    """Work orders for maintenance activities"""
    
    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    # Identification
    order_number = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    
    # Related entities
    maintenance_task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='work_orders', null=True, blank=True)
    issues = models.ManyToManyField('maintenance.Issue', related_name='work_orders', blank=True)
    
    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='draft')

    PRIORITY_CHOICES = [
    ('critical', 'Critical'),
    ('high', 'High'),
    ('medium', 'Medium'),
    ('low', 'Low'),
    ]

    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    
    # Assignment
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='supervised_work_orders')
    assigned_team = models.ForeignKey('utilities.Team', on_delete=models.SET_NULL, null=True, related_name='work_orders')
    
    # Instructions
    instructions = models.TextField()
    safety_requirements = models.TextField(blank=True)
    
    # Resources
    estimated_labor_hours = models.FloatField(default=0)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Approval
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_work_orders')
    approved_at = models.DateTimeField(null=True, blank=True)
    
    # Completion
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_work_orders')
    completed_at = models.DateTimeField(null=True, blank=True)
    actual_labor_hours = models.FloatField(null=True, blank=True)
    actual_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    
    # Metadata
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_work_orders')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'work_orders'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.order_number} - {self.title}"


class IssuePhoto(models.Model):
    """Photos attached to issues"""
    issue = models.ForeignKey('maintenance.Issue', on_delete=models.CASCADE, related_name='photos')
    image = models.ImageField(upload_to='issue_photos/')
    caption = models.CharField(max_length=200, blank=True)
    
    # Photo metadata
    is_before_repair = models.BooleanField(default=True)
    
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'issue_photos'
        ordering = ['uploaded_at']
    
    def __str__(self):
        return f"Photo for {self.issue.issue_id}"


class MaintenanceLog(models.Model):
    """Activity logs for maintenance work"""
    
    LOG_TYPE_CHOICES = [
        ('status_change', 'Status Change'),
        ('assignment', 'Assignment'),
        ('work_update', 'Work Update'),
        ('photo_added', 'Photo Added'),
        ('comment', 'Comment'),
    ]
    
    # Related entities
    issue = models.ForeignKey('maintenance.Issue', on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    maintenance_task = models.ForeignKey(MaintenanceTask, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    work_order = models.ForeignKey(WorkOrder, on_delete=models.CASCADE, related_name='logs', null=True, blank=True)
    
    # Log details
    log_type = models.CharField(max_length=20, choices=LOG_TYPE_CHOICES)
    message = models.TextField()
    
    # Additional data (JSON field for flexibility)
    data = models.JSONField(default=dict, blank=True)
    
    # User tracking
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'maintenance_logs'
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.log_type} - {self.created_at}"
    

class Team(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    members = models.ManyToManyField('utilities.User', related_name='teams')


class Department(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('utilities.User', on_delete=models.SET_NULL, null=True, related_name='managed_departments')
    teams = models.ManyToManyField('utilities.Team', related_name='departments')


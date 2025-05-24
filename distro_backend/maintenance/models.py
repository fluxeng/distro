from django.db import models
from django.contrib.gis.db import models as gis_models
from utilities.models import User, Team
from infrastructure.models import Asset
from customer_support.models import Ticket

class Issue(models.Model):
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('verified', 'Verified'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('critical', 'Critical'),
    ]
    ISSUE_TYPE_CHOICES = [
        ('leak', 'Leak'),
        ('break', 'Break'),
        ('blockage', 'Blockage'),
        ('equipment_failure', 'Equipment Failure'),
        ('other', 'Other'),
    ]
    issue_id = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    location = gis_models.PointField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='medium')
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    reported_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_issues')
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    customer_ticket = models.ForeignKey(Ticket, on_delete=models.SET_NULL, null=True, blank=True, related_name='related_issues')
    class Meta:
        db_table = 'issues'
        indexes = [
            models.Index(fields=['issue_id'], name='issues_issue_i_270845_idx'),
            models.Index(fields=['status'], name='issues_status_ba6d29_idx'),
            models.Index(fields=['priority'], name='issues_priorit_9e4563_idx'),
            models.Index(fields=['issue_type'], name='issues_issue_t_912892_idx'),
        ]
    def __str__(self):
        return f"Issue {self.issue_id} - {self.issue_type}"

class IssuePhoto(models.Model):
    issue = models.ForeignKey(Issue, on_delete=models.CASCADE, related_name='photos')
    photo = models.ImageField(upload_to='issue_photos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='uploaded_issue_photos')
    class Meta:
        db_table = 'issue_photos'
    def __str__(self):
        return f"Photo for Issue {self.issue.issue_id}"

class MaintenanceLog(models.Model):
    description = models.TextField()
    log_type = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='maintenance_logs')
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_logs')
    maintenance_task = models.ForeignKey('MaintenanceTask', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_logs')
    work_order = models.ForeignKey('WorkOrder', on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_logs')
    class Meta:
        db_table = 'maintenance_logs'
    def __str__(self):
        return f"Log {self.id} - {self.log_type}"

class MaintenanceTask(models.Model):
    STATUS_CHOICES = [
        ('scheduled', 'Scheduled'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    task_id = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    scheduled_date = models.DateTimeField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='scheduled')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name='maintenance_tasks')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_maintenance_tasks')
    issue = models.ForeignKey(Issue, on_delete=models.SET_NULL, null=True, blank=True, related_name='maintenance_tasks')
    class Meta:
        db_table = 'maintenance_tasks'
    def __str__(self):
        return f"Task {self.task_id}"

class WorkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    work_order_id = models.CharField(max_length=20, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='approved_work_orders')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    completed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='completed_work_orders')
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_work_orders')
    issues = models.ManyToManyField(Issue, related_name='work_orders')
    maintenance_task = models.ForeignKey(MaintenanceTask, on_delete=models.SET_NULL, null=True, blank=True, related_name='work_orders')
    supervisor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='supervised_work_orders')
    class Meta:
        db_table = 'work_orders'
    def __str__(self):
        return f"Work Order {self.work_order_id}"
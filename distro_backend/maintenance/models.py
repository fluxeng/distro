# maintenance/models.py
from django.db import models
from django.contrib.gis.db import models as gis_models
from utilities.models import User, Team
from infrastructure.models import Asset, Pipe, Zone


class Issue(models.Model):
    """Issues reported in the field"""
    
    ISSUE_TYPE_CHOICES = [
        ('leak', 'Leak'),
        ('burst', 'Pipe Burst'),
        ('blockage', 'Blockage'),
        ('quality', 'Water Quality'),
        ('pressure', 'Low Pressure'),
        ('meter', 'Meter Problem'),
        ('valve', 'Valve Issue'),
        ('other', 'Other'),
    ]
    
    PRIORITY_CHOICES = [
        ('critical', 'Critical'),
        ('high', 'High'),
        ('medium', 'Medium'),
        ('low', 'Low'),
    ]
    
    STATUS_CHOICES = [
        ('reported', 'Reported'),
        ('verified', 'Verified'),
        ('assigned', 'Assigned'),
        ('in_progress', 'In Progress'),
        ('resolved', 'Resolved'),
        ('closed', 'Closed'),
    ]
    
    # Identification
    issue_id = models.CharField(max_length=50, unique=True)
    title = models.CharField(max_length=200)
    description = models.TextField()
    
    # Classification
    issue_type = models.CharField(max_length=20, choices=ISSUE_TYPE_CHOICES)
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='reported')
    
    # Location
    location = gis_models.PointField()
    address = models.TextField(blank=True)
    landmark = models.CharField(max_length=200, blank=True)
    
    # Related infrastructure
    affected_asset = models.ForeignKey(Asset, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    affected_pipe = models.ForeignKey(Pipe, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    affected_zone = models.ForeignKey(Zone, on_delete=models.SET_NULL, null=True, blank=True, related_name='issues')
    
    # Reporting
    reported_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='reported_issues')
    reported_at = models.DateTimeField(auto_now_add=True)
    reported_via = models.CharField(max_length=20, choices=[
        ('field', 'Field Report'),
        ('customer', 'Customer Report'),
        ('monitoring', 'System Monitoring'),
        ('inspection', 'Routine Inspection'),
    ], default='field')
    
    # Customer link (if reported by customer)
    customer_ticket = models.ForeignKey('customer_support.Ticket', on_delete=models.SET_NULL, null=True, blank=True, related_name='related_issues')
    
    # Verification
    verified_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='verified_issues')
    verified_at = models.DateTimeField(null=True, blank=True)
    verification_notes = models.TextField(blank=True)
    
    # Assignment
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    assigned_team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    assigned_at = models.DateTimeField(null=True, blank=True)
    
    # Resolution
    resolved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='resolved_issues')
    resolved_at = models.DateTimeField(null=True, blank=True)
    resolution_notes = models.TextField(blank=True)
    
    # Impact assessment
    estimated_affected_customers = models.IntegerField(default=0)
    water_loss_estimate = models.FloatField(default=0, help_text="Estimated water loss in liters")
    
    # Timestamps
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'issues'
        ordering = ['-reported_at']
        indexes = [
            models.Index(fields=['issue_id']),
            models.Index(fields=['status']),
            models.Index(fields=['priority']),
            models.Index(fields=['issue_type']),
        ]
    
    def __str__(self):
        return f"{self.issue_id} - {self.title}"
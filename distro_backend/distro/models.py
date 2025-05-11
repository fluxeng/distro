from django.contrib.gis.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import JSONField  # Updated import
from django.utils import timezone

class UserProfile(AbstractUser):
    ROLE_CHOICES = (
        ('ADMIN', 'Admin'),
        ('SUPERVISOR', 'Supervisor'),
        ('FIELD_TECHNICIAN', 'Field Technician'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='FIELD_TECHNICIAN')
    phone_number = models.CharField(max_length=15, blank=True)
    push_token = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = 'user_profile'

class AssetType(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'asset_type'

class Asset(models.Model):
    name = models.CharField(max_length=100)
    asset_type = models.ForeignKey(AssetType, on_delete=models.CASCADE)
    geometry = models.GeometryField()
    metadata = JSONField(default=dict)  # Updated field
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'asset'

class Issue(models.Model):
    PRIORITY_CHOICES = (
        ('LOW', 'Low'),
        ('MEDIUM', 'Medium'),
        ('HIGH', 'High'),
    )
    STATUS_CHOICES = (
        ('OPEN', 'Open'),
        ('IN_PROGRESS', 'In Progress'),
        ('RESOLVED', 'Resolved'),
    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='LOW')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='OPEN')
    location = models.PointField()
    reported_by = models.ForeignKey(UserProfile, on_delete=models.CASCADE, related_name='reported_issues')
    assigned_to = models.ForeignKey(UserProfile, on_delete=models.SET_NULL, null=True, blank=True, related_name='assigned_issues')
    reported_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title

    class Meta:
        db_table = 'issue'

class IssueImage(models.Model):
    issue = models.ForeignKey(Issue, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='issue_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'issue_image'
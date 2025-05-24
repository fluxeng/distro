from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.gis.db import models as gis_models
from django.core.validators import MinValueValidator, MaxValueValidator
from tenants.models import Utility

class User(AbstractUser):
    """Custom user model with additional fields"""
    
    ROLE_CHOICES = [
        ('admin', 'Administrator'),
        ('supervisor', 'Supervisor'),
        ('field_agent', 'Field Agent'),
        ('customer_service', 'Customer Service'),
        ('billing', 'Billing Officer'),
        ('technician', 'Technician'),
    ]
    
    phone_number = models.CharField(max_length=15, blank=True)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='field_agent')
    department = models.ForeignKey('utilities.Department', on_delete=models.SET_NULL, null=True, blank=True, related_name='staff')
    profile_picture = models.ImageField(upload_to='profiles/', null=True, blank=True)
    is_field_agent = models.BooleanField(default=False)
    current_location = gis_models.PointField(null=True, blank=True)
    location_updated_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Utility, on_delete=models.CASCADE, null=True, blank=True, related_name='users')
    
    class Meta:
        db_table = 'users'
    
    def __str__(self):
        return self.get_full_name() or self.username

class Department(models.Model):
    """Departments within the utility"""
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    manager = models.ForeignKey('utilities.User', on_delete=models.SET_NULL, null=True, related_name='managed_departments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Utility, on_delete=models.CASCADE, null=True, blank=True, related_name='departments')
    
    class Meta:
        db_table = 'departments'
    
    def __str__(self):
        return self.name

class Team(models.Model):
    """Teams for organizing field agents"""
    name = models.CharField(max_length=100)
    department = models.ForeignKey('utilities.Department', on_delete=models.CASCADE, related_name='teams')
    supervisor = models.ForeignKey('utilities.User', on_delete=models.SET_NULL, null=True, related_name='supervised_teams')
    members = models.ManyToManyField('utilities.User', related_name='teams')
    coverage_area = gis_models.PolygonField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    tenant = models.ForeignKey(Utility, on_delete=models.CASCADE, null=True, blank=True, related_name='teams')
    
    class Meta:
        db_table = 'teams'
    
    def __str__(self):
        return f"{self.name} - {self.department.name}"
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin

class Utility(TenantMixin):
    """Water utility tenants"""
    
    SUBSCRIPTION_TIER_CHOICES = [
        ('basic', 'Basic'),
        ('standard', 'Standard'),
        ('premium', 'Premium'),
    ]
    
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True, db_index=True)
    description = models.TextField(blank=True)
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)
    address = models.TextField(blank=True)
    subscription_tier = models.CharField(max_length=20, choices=SUBSCRIPTION_TIER_CHOICES, default='basic')
    is_active = models.BooleanField(default=True)
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Auto-create schema on save
    auto_create_schema = True
    
    class Meta:
        db_table = 'utilities'
    
    def __str__(self):
        return self.name

class Domain(DomainMixin):
    """Domains for tenant access"""
    
    class Meta:
        db_table = 'domains'
    
    def __str__(self):
        return self.domain
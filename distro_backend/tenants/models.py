# tenants/models.py
from django.db import models
from django_tenants.models import TenantMixin, DomainMixin
from django.contrib.gis.db import models as gis_models


class Utility(TenantMixin):
    """
    Water utility tenant model
    Each utility gets its own isolated database schema
    """
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Contact information
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=20)
    address = models.TextField()
    
    # Geographic coverage area
    service_area = gis_models.PolygonField(null=True, blank=True)
    
    # Branding customization
    logo = models.ImageField(upload_to='utility_logos/', null=True, blank=True)
    primary_color = models.CharField(max_length=7, default='#1f2937')  # hex color
    secondary_color = models.CharField(max_length=7, default='#3b82f6')
    
    # Subscription and billing
    subscription_tier = models.CharField(
        max_length=20,
        choices=[
            ('basic', 'Basic'),
            ('professional', 'Professional'),
            ('enterprise', 'Enterprise'),
        ],
        default='basic'
    )
    max_field_agents = models.PositiveIntegerField(default=10)
    max_assets = models.PositiveIntegerField(default=1000)
    
    # Timestamps
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    
    # Tenant status
    is_active = models.BooleanField(default=True)
    
    # Auto-generated schema name based on utility name
    auto_create_schema = True
    
    class Meta:
        verbose_name = "Water Utility"
        verbose_name_plural = "Water Utilities"
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Generate schema name from utility name if not set
        if not self.schema_name:
            import re
            schema_name = re.sub(r'[^a-zA-Z0-9]', '_', self.name.lower())
            schema_name = f"utility_{schema_name}"
            self.schema_name = schema_name
        super().save(*args, **kwargs)


class Domain(DomainMixin):
    """
    Domain model for each utility
    Handles subdomain routing to correct tenant schema
    """
    pass

    class Meta:
        verbose_name = "Utility Domain"
        verbose_name_plural = "Utility Domains"
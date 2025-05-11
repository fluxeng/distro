from django_tenants.models import TenantMixin, DomainMixin
from django.db import models

class Tenant(TenantMixin):
    name = models.CharField(max_length=100)
    schema_name = models.CharField(max_length=63, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    auto_create_schema = True
    auto_drop_schema = True  # Enable schema deletion

    class Meta:
        db_table = 'tenant'

    def __str__(self):
        return self.name

class Domain(DomainMixin):
    class Meta:
        db_table = 'domain'
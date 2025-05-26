#!/usr/bin/env python
"""
Debug script to check current schema context
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distro_backend.settings')
django.setup()

from django.db import connection
from tenants.models import Utility, Domain

def check_current_schema():
    """Check what schema Django is currently using"""
    print("🔍 Current Database Context:")
    print(f"   Current schema: {getattr(connection, 'schema_name', 'NOT SET')}")
    print(f"   Database name: {connection.settings_dict['NAME']}")
    
    # Try to get schema from connection
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT current_schema();")
            current_schema = cursor.fetchone()[0]
            print(f"   PostgreSQL current_schema(): {current_schema}")
    except Exception as e:
        print(f"   ❌ Error getting current schema: {e}")

def check_all_tenants():
    """List all tenants and their domains"""
    print("\n🏢 All Tenants:")
    try:
        tenants = Utility.objects.all()
        for tenant in tenants:
            print(f"   - {tenant.name}")
            print(f"     Schema: {tenant.schema_name}")
            print(f"     Active: {tenant.is_active}")
            print(f"     Domains:")
            for domain in tenant.domains.all():
                print(f"       → {domain.domain} {'(primary)' if domain.is_primary else ''} {'(active)' if domain.is_active else '(inactive)'}")
            print()
    except Exception as e:
        print(f"   ❌ Error getting tenants: {e}")

def test_schema_access():
    """Test accessing tables in different schemas"""
    print("🧪 Testing Schema Access:")
    
    # Test accessing zones in current context
    try:
        from infrastructure.models import Zone
        zones = Zone.objects.all()
        print(f"   ✅ Can access zones in current context: {zones.count()} zones found")
    except Exception as e:
        print(f"   ❌ Cannot access zones in current context: {e}")
    
    # Test with specific schema context
    try:
        from django_tenants.utils import schema_context
        with schema_context('demo'):
            zones = Zone.objects.all()
            print(f"   ✅ Can access zones in 'demo' schema: {zones.count()} zones found")
    except Exception as e:
        print(f"   ❌ Cannot access zones in 'demo' schema: {e}")

def check_domain_routing():
    """Check domain-to-tenant routing"""
    print("\n🌐 Domain Routing Check:")
    
    domains_to_test = [
        'localhost',
        '127.0.0.1',
        'demo.localhost',
    ]
    
    for domain_name in domains_to_test:
        try:
            domain = Domain.objects.filter(domain=domain_name).first()
            if domain:
                print(f"   {domain_name} → {domain.tenant.schema_name} ({domain.tenant.name})")
            else:
                print(f"   {domain_name} → No tenant found")
        except Exception as e:
            print(f"   {domain_name} → Error: {e}")

if __name__ == "__main__":
    check_current_schema()
    check_all_tenants()
    test_schema_access()
    check_domain_routing()

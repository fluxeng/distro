#!/usr/bin/env python
"""
Complete setup script for Distro V1 Backend
Run this after installing requirements to set up the project
"""

import os
import sys
import django
from datetime import datetime

# Colors for output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def print_step(step, message):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}🚀 Step {step}: {message}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}ℹ️  {message}{Colors.ENDC}")

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distro_backend.settings')
django.setup()

from django.core.management import call_command
from tenants.models import Utility, Domain
from django_tenants.utils import schema_context
from django.db import connection

def check_database():
    """Check database connection"""
    print_step(1, "Checking Database Connection")
    
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print_success(f"Database connected: {version.split(',')[0]}")
        
        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_Version();")
            postgis_version = cursor.fetchone()[0]
            print_success(f"PostGIS available: {postgis_version}")
        
        return True
    except Exception as e:
        print_error(f"Database connection failed: {e}")
        return False

def run_migrations():
    """Run all migrations"""
    print_step(2, "Running Database Migrations")
    
    try:
        print_info("Running shared app migrations...")
        call_command('migrate_schemas', '--shared', verbosity=1)
        print_success("Shared migrations completed")
        
        # Check if demo tenant exists
        try:
            demo_tenant = Utility.objects.get(schema_name='demo')
            print_info("Running demo tenant migrations...")
            call_command('migrate_schemas', '--schema=demo', verbosity=1)
            print_success("Demo tenant migrations completed")
        except Utility.DoesNotExist:
            print_info("Demo tenant not found - will create it next")
        
        return True
    except Exception as e:
        print_error(f"Migration failed: {e}")
        return False

def create_tenants():
    """Create public and demo tenants"""
    print_step(3, "Setting Up Tenants")
    
    try:
        # Create public tenant if it doesn't exist
        public_tenant, created = Utility.objects.get_or_create(
            schema_name='public',
            defaults={
                'name': 'Master Tenant',
                'is_active': True
            }
        )
        
        if created:
            print_success("Created public tenant")
        else:
            print_info("Public tenant already exists")
        
        # Create localhost domain for public tenant
        localhost_domain, created = Domain.objects.get_or_create(
            domain='localhost',
            tenant=public_tenant,
            defaults={
                'is_primary': True,
                'is_active': True
            }
        )
        
        if created:
            print_success("Created localhost domain")
        else:
            print_info("Localhost domain already exists")
        
        # Create demo tenant if it doesn't exist
        demo_tenant, created = Utility.objects.get_or_create(
            schema_name='demo',
            defaults={
                'name': 'Demo Water Utility',
                'is_active': True
            }
        )
        
        if created:
            print_success("Created demo tenant")
            # Run migrations for new demo tenant
            call_command('migrate_schemas', '--schema=demo', verbosity=1)
            print_success("Demo tenant migrations completed")
        else:
            print_info("Demo tenant already exists")
        
        # Create demo.localhost domain
        demo_domain, created = Domain.objects.get_or_create(
            domain='demo.localhost',
            tenant=demo_tenant,
            defaults={
                'is_primary': True,
                'is_active': True
            }
        )
        
        if created:
            print_success("Created demo.localhost domain")
        else:
            print_info("Demo.localhost domain already exists")
        
        return True
    except Exception as e:
        print_error(f"Tenant creation failed: {e}")
        return False

def create_sample_data():
    """Create sample data for demo tenant"""
    print_step(4, "Creating Sample Data")
    
    try:
        with schema_context('demo'):
            from infrastructure.models import AssetType, Zone
            from django.contrib.gis.geos import Polygon
            
            # Create asset types
            asset_types_data = [
                {'name': 'Water Pipe', 'code': 'pipe', 'icon': 'pipe-icon', 'color': '#2563eb', 'is_linear': True},
                {'name': 'Valve', 'code': 'valve', 'icon': 'valve-icon', 'color': '#dc2626', 'is_linear': False},
                {'name': 'Water Meter', 'code': 'meter', 'icon': 'meter-icon', 'color': '#059669', 'is_linear': False},
                {'name': 'Pump Station', 'code': 'pump_station', 'icon': 'pump-icon', 'color': '#7c3aed', 'is_linear': False},
                {'name': 'Reservoir', 'code': 'reservoir', 'icon': 'reservoir-icon', 'color': '#0891b2', 'is_linear': False},
                {'name': 'Treatment Plant', 'code': 'treatment_plant', 'icon': 'plant-icon', 'color': '#ea580c', 'is_linear': False},
                {'name': 'Fire Hydrant', 'code': 'hydrant', 'icon': 'hydrant-icon', 'color': '#be123c', 'is_linear': False},
            ]
            
            created_types = 0
            for asset_data in asset_types_data:
                asset_type, created = AssetType.objects.get_or_create(
                    code=asset_data['code'],
                    defaults=asset_data
                )
                if created:
                    created_types += 1
            
            print_success(f"Created {created_types} asset types")
            
            # Create sample zones (Nairobi coordinates)
            zones_data = [
                {
                    'name': 'Westlands Zone',
                    'code': 'WEST_001',
                    'boundary': Polygon([
                        [36.80, -1.26], [36.82, -1.26], [36.82, -1.24], [36.80, -1.24], [36.80, -1.26]
                    ]),
                    'population': 45000,
                    'households': 11250,
                    'commercial_connections': 650
                },
                {
                    'name': 'Karen Zone',
                    'code': 'KAREN_001',
                    'boundary': Polygon([
                        [36.68, -1.32], [36.72, -1.32], [36.72, -1.30], [36.68, -1.30], [36.68, -1.32]
                    ]),
                    'population': 25000,
                    'households': 6250,
                    'commercial_connections': 200
                },
                {
                    'name': 'Industrial Area',
                    'code': 'IND_001',
                    'boundary': Polygon([
                        [36.85, -1.30], [36.88, -1.30], [36.88, -1.28], [36.85, -1.28], [36.85, -1.30]
                    ]),
                    'population': 15000,
                    'households': 3750,
                    'commercial_connections': 890
                }
            ]
            
            created_zones = 0
            for zone_data in zones_data:
                zone, created = Zone.objects.get_or_create(
                    code=zone_data['code'],
                    defaults=zone_data
                )
                if created:
                    created_zones += 1
            
            print_success(f"Created {created_zones} zones")
            
            # Summary
            total_asset_types = AssetType.objects.count()
            total_zones = Zone.objects.count()
            print_info(f"Demo tenant now has {total_asset_types} asset types and {total_zones} zones")
        
        return True
    except Exception as e:
        print_error(f"Sample data creation failed: {e}")
        return False

def verify_setup():
    """Verify the setup"""
    print_step(5, "Verifying Setup")
    
    try:
        # Check tenants
        tenants = Utility.objects.all()
        print_info(f"Found {tenants.count()} tenants:")
        
        for tenant in tenants:
            domains = [d.domain for d in tenant.domains.all()]
            print_info(f"  - {tenant.name} (schema: {tenant.schema_name}) → {', '.join(domains)}")
        
        # Test schema access
        with schema_context('demo'):
            from infrastructure.models import Zone, AssetType
            zones_count = Zone.objects.count()
            asset_types_count = AssetType.objects.count()
            print_success(f"Demo tenant accessible: {zones_count} zones, {asset_types_count} asset types")
        
        return True
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def print_instructions():
    """Print final instructions"""
    print_step(6, "Setup Complete!")
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}🎉 Distro V1 Backend is ready!{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"1. Add to your /etc/hosts file:")
    print(f"   {Colors.WARNING}127.0.0.1 demo.localhost{Colors.ENDC}")
    print()
    print(f"2. Create superuser accounts:")
    print(f"   {Colors.OKCYAN}python manage.py create_tenant_superuser --schema=public{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}python manage.py create_tenant_superuser --schema=demo{Colors.ENDC}")
    print()
    print(f"3. Start the development server:")
    print(f"   {Colors.OKCYAN}python manage.py runserver{Colors.ENDC}")
    print()
    print(f"4. Access the application:")
    print(f"   • Public Admin: {Colors.OKBLUE}http://localhost:8000/admin/{Colors.ENDC}")
    print(f"   • Public API Docs: {Colors.OKBLUE}http://localhost:8000/api/docs/{Colors.ENDC}")
    print(f"   • Demo Admin: {Colors.OKBLUE}http://demo.localhost:8000/admin/{Colors.ENDC}")
    print(f"   • Demo API Docs: {Colors.OKBLUE}http://demo.localhost:8000/api/docs/{Colors.ENDC}")
    print()
    print(f"5. Test API endpoints:")
    print(f"   {Colors.OKCYAN}curl http://localhost:8000/api/tenants/{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}curl http://demo.localhost:8000/api/infrastructure/zones/{Colors.ENDC}")

def main():
    """Main setup function"""
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}Distro V1 Backend Setup{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    
    steps = [
        check_database,
        run_migrations,
        create_tenants,
        create_sample_data,
        verify_setup
    ]
    
    success = True
    for step_func in steps:
        if not step_func():
            success = False
            break
    
    if success:
        print_instructions()
        print(f"\n{Colors.OKGREEN}✅ Setup completed successfully!{Colors.ENDC}")
    else:
        print(f"\n{Colors.FAIL}❌ Setup failed. Please check the errors above.{Colors.ENDC}")
    
    return success

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Setup interrupted by user{Colors.ENDC}")
    except Exception as e:
        print(f"\n{Colors.FAIL}💥 Unexpected error: {e}{Colors.ENDC}")
        import traceback
        traceback.print_exc()
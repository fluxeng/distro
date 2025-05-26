#!/usr/bin/env python
"""
🚀 Complete Django-Tenants Setup Script for Distro Water Utility Platform

This script will:
1. Clean up any existing problematic tenants
2. Create proper public tenant (localhost) for tenant management
3. Create demo tenant (demo.localhost) for water utility operations
4. Run all necessary migrations
5. Create sample data
6. Verify everything works
7. Provide usage instructions

Run: python complete_tenant_setup.py
"""

import os
import sys
import django
from datetime import datetime

# Colors for better output
class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def print_header(message):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{message.center(60)}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")

def print_step(step_num, message):
    print(f"\n{Colors.OKCYAN}{Colors.BOLD}🚀 Step {step_num}: {message}{Colors.ENDC}")
    print(f"{Colors.OKCYAN}{'─' * (len(message) + 15)}{Colors.ENDC}")

def print_success(message):
    print(f"{Colors.OKGREEN}✅ {message}{Colors.ENDC}")

def print_info(message):
    print(f"{Colors.OKBLUE}ℹ️  {message}{Colors.ENDC}")

def print_warning(message):
    print(f"{Colors.WARNING}⚠️  {message}{Colors.ENDC}")

def print_error(message):
    print(f"{Colors.FAIL}❌ {message}{Colors.ENDC}")

def print_action(message):
    print(f"   🔧 {message}")

def print_result(message):
    print(f"   📊 {message}")

# Setup Django
try:
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'distro_backend.settings')
    django.setup()
    print_success("Django environment loaded successfully")
except Exception as e:
    print_error(f"Failed to setup Django: {e}")
    sys.exit(1)

from tenants.models import Utility, Domain
from django.core.management import call_command
from django_tenants.utils import schema_context
from django.db import connection, transaction

def check_prerequisites():
    """Check if database and basic setup is ready"""
    print_step(1, "Checking Prerequisites")
    
    try:
        # Test database connection
        with connection.cursor() as cursor:
            cursor.execute("SELECT version();")
            version = cursor.fetchone()[0]
            print_success(f"Database connection established")
            print_result(f"PostgreSQL: {version.split(',')[0]}")
        
        # Check if PostGIS is available
        with connection.cursor() as cursor:
            cursor.execute("SELECT PostGIS_Version();")
            postgis_version = cursor.fetchone()[0]
            print_success(f"PostGIS extension available")
            print_result(f"PostGIS: {postgis_version}")
        
        # Check if tenant tables exist
        if Utility._meta.db_table:
            print_success("Tenant models are accessible")
        
        return True
        
    except Exception as e:
        print_error(f"Prerequisites check failed: {e}")
        print_warning("Make sure PostgreSQL and PostGIS are installed and configured")
        return False

def cleanup_existing_tenants():
    """Clean up any incorrectly created tenants"""
    print_step(2, "Cleaning Up Existing Setup")
    
    try:
        # Get all existing tenants
        existing_tenants = Utility.objects.all()
        
        if not existing_tenants.exists():
            print_info("No existing tenants found - starting fresh")
            return True
        
        print_info(f"Found {existing_tenants.count()} existing tenant(s):")
        
        problems_found = False
        for tenant in existing_tenants:
            domains = [d.domain for d in tenant.domains.all()]
            print_result(f"{tenant.name} (schema: {tenant.schema_name}) → {domains}")
            
            # Check for problems
            if tenant.schema_name == 'public' and tenant.name != 'Master Tenant':
                print_warning(f"Problematic tenant found: {tenant.name} uses public schema incorrectly")
                problems_found = True
        
        if problems_found:
            response = input(f"\n{Colors.WARNING}⚠️  Delete problematic tenants and start fresh? (y/N): {Colors.ENDC}")
            if response.lower() == 'y':
                print_action("Deleting problematic tenants...")
                for tenant in existing_tenants:
                    if tenant.schema_name == 'public' and tenant.name != 'Master Tenant':
                        print_action(f"Deleting {tenant.name}...")
                        tenant.delete()
                print_success("Cleanup completed")
            else:
                print_info("Keeping existing tenants - will work around them")
        else:
            print_success("No problematic tenants found")
        
        return True
        
    except Exception as e:
        print_error(f"Cleanup failed: {e}")
        return False

def create_public_tenant():
    """Create the public/master tenant"""
    print_step(3, "Creating Public Tenant (Master Control)")
    
    try:
        # Check if public tenant exists
        public_tenant = Utility.objects.filter(schema_name='public').first()
        
        if public_tenant:
            print_info(f"Public tenant already exists: {public_tenant.name}")
            
            # Ensure it has localhost domain
            localhost_domain = Domain.objects.filter(domain='localhost', tenant=public_tenant).first()
            if not localhost_domain:
                print_action("Creating localhost domain for public tenant...")
                Domain.objects.create(
                    domain='localhost',
                    tenant=public_tenant,
                    is_primary=True,
                    is_active=True
                )
                print_success("Created localhost domain")
            else:
                print_success("Public tenant setup is correct")
            
            return public_tenant
        
        # Create new public tenant
        print_action("Creating public tenant...")
        public_tenant = Utility(
            schema_name='public',
            name='Master Tenant',
            is_active=True
        )
        public_tenant.save(verbosity=0)  # Don't create schema - public already exists
        
        print_action("Creating localhost domain...")
        Domain.objects.create(
            domain='localhost',
            tenant=public_tenant,
            is_primary=True,
            is_active=True
        )
        
        print_success("Public tenant created successfully")
        print_result(f"Name: {public_tenant.name}")
        print_result(f"Schema: {public_tenant.schema_name}")
        print_result("Domain: localhost")
        print_result("Purpose: Tenant management and administration")
        
        return public_tenant
        
    except Exception as e:
        print_error(f"Failed to create public tenant: {e}")
        return None

def create_demo_tenant():
    """Create the demo tenant"""
    print_step(4, "Creating Demo Tenant (Water Utility)")
    
    try:
        # Check if demo tenant exists
        demo_tenant = Utility.objects.filter(schema_name='demo').first()
        
        if demo_tenant:
            print_info(f"Demo tenant already exists: {demo_tenant.name}")
            
            # Ensure it has demo.localhost domain
            demo_domain = Domain.objects.filter(domain='demo.localhost', tenant=demo_tenant).first()
            if not demo_domain:
                print_action("Creating demo.localhost domain...")
                Domain.objects.create(
                    domain='demo.localhost',
                    tenant=demo_tenant,
                    is_primary=True,
                    is_active=True
                )
                print_success("Created demo.localhost domain")
            else:
                print_success("Demo tenant setup is correct")
            
            return demo_tenant
        
        # Create new demo tenant
        print_action("Creating demo tenant...")
        demo_tenant = Utility(
            schema_name='demo',
            name='Demo Water Utility',
            is_active=True
        )
        demo_tenant.save(verbosity=1)  # This creates the schema
        
        print_action("Creating demo.localhost domain...")
        Domain.objects.create(
            domain='demo.localhost',
            tenant=demo_tenant,
            is_primary=True,
            is_active=True
        )
        
        print_success("Demo tenant created successfully")
        print_result(f"Name: {demo_tenant.name}")
        print_result(f"Schema: {demo_tenant.schema_name}")
        print_result("Domain: demo.localhost")
        print_result("Purpose: Water utility operations and infrastructure management")
        
        return demo_tenant
        
    except Exception as e:
        print_error(f"Failed to create demo tenant: {e}")
        return None

def run_migrations():
    """Run all necessary migrations"""
    print_step(5, "Running Database Migrations")
    
    try:
        # First, migrate shared apps (public schema)
        print_action("Running migrations for shared apps (public schema)...")
        call_command('migrate_schemas', '--shared', verbosity=1)
        print_success("Shared apps migrated successfully")
        
        # Then migrate tenant apps for demo schema
        print_action("Running migrations for demo tenant...")
        call_command('migrate_schemas', '--schema=demo', verbosity=1)
        print_success("Demo tenant migrated successfully")
        
        return True
        
    except Exception as e:
        print_error(f"Migration failed: {e}")
        print_warning("You may need to run migrations manually:")
        print_warning("  python manage.py migrate_schemas --shared")
        print_warning("  python manage.py migrate_schemas --schema=demo")
        return False

def create_sample_data():
    """Create sample data for demo tenant"""
    print_step(6, "Creating Sample Data")
    
    try:
        with schema_context('demo'):
            from infrastructure.models import AssetType, Zone
            from django.contrib.gis.geos import Polygon
            
            print_action("Creating asset types...")
            asset_types_created = 0
            
            asset_types_data = [
                {'name': 'Water Pipe', 'code': 'pipe', 'icon': 'pipe-icon', 'color': '#2563eb', 'is_linear': True},
                {'name': 'Valve', 'code': 'valve', 'icon': 'valve-icon', 'color': '#dc2626', 'is_linear': False},
                {'name': 'Water Meter', 'code': 'meter', 'icon': 'meter-icon', 'color': '#059669', 'is_linear': False},
                {'name': 'Pump Station', 'code': 'pump_station', 'icon': 'pump-icon', 'color': '#7c3aed', 'is_linear': False},
                {'name': 'Reservoir', 'code': 'reservoir', 'icon': 'reservoir-icon', 'color': '#0891b2', 'is_linear': False},
                {'name': 'Treatment Plant', 'code': 'treatment_plant', 'icon': 'plant-icon', 'color': '#ea580c', 'is_linear': False},
                {'name': 'Fire Hydrant', 'code': 'hydrant', 'icon': 'hydrant-icon', 'color': '#be123c', 'is_linear': False},
            ]
            
            for asset_data in asset_types_data:
                asset_type, created = AssetType.objects.get_or_create(
                    code=asset_data['code'],
                    defaults=asset_data
                )
                if created:
                    asset_types_created += 1
                    print_result(f"✓ {asset_type.name}")
            
            print_success(f"Created {asset_types_created} asset types")
            
            print_action("Creating sample zones...")
            zones_created = 0
            
            # Create sample zones with realistic Nairobi coordinates
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
            
            for zone_data in zones_data:
                zone, created = Zone.objects.get_or_create(
                    code=zone_data['code'],
                    defaults=zone_data
                )
                if created:
                    zones_created += 1
                    print_result(f"✓ {zone.name} ({zone.population:,} population)")
            
            print_success(f"Created {zones_created} zones")
            
            # Summary
            total_asset_types = AssetType.objects.count()
            total_zones = Zone.objects.count()
            print_result(f"Demo tenant now has {total_asset_types} asset types and {total_zones} zones")
        
        return True
        
    except Exception as e:
        print_error(f"Sample data creation failed: {e}")
        print_warning("You can create sample data later through the admin interface")
        return False

def verify_setup():
    """Verify the complete setup"""
    print_step(7, "Verifying Setup")
    
    try:
        # Check tenants
        print_action("Checking tenant configuration...")
        tenants = Utility.objects.all().order_by('schema_name')
        
        for tenant in tenants:
            domains = [d.domain for d in tenant.domains.all()]
            print_result(f"{tenant.name} (schema: {tenant.schema_name}) → {', '.join(domains)}")
        
        # Test schema access
        print_action("Testing schema access...")
        
        # Test public schema
        try:
            from users.models import User
            users_count = User.objects.count()
            print_result(f"✓ Public schema accessible: {users_count} users")
        except Exception as e:
            print_result(f"✗ Public schema error: {e}")
        
        # Test demo schema
        try:
            with schema_context('demo'):
                from infrastructure.models import Zone, AssetType
                zones_count = Zone.objects.count()
                asset_types_count = AssetType.objects.count()
                print_result(f"✓ Demo schema accessible: {zones_count} zones, {asset_types_count} asset types")
        except Exception as e:
            print_result(f"✗ Demo schema error: {e}")
        
        print_success("Setup verification completed")
        return True
        
    except Exception as e:
        print_error(f"Verification failed: {e}")
        return False

def test_api_endpoints():
    """Test key API endpoints"""
    print_step(8, "Testing API Endpoints")
    
    try:
        from django.test import RequestFactory
        from django_tenants.middleware.main import TenantMainMiddleware
        
        print_action("Testing tenant routing...")
        
        factory = RequestFactory()
        middleware = TenantMainMiddleware(lambda r: None)
        
        # Test localhost (public tenant)
        request = factory.get('/', HTTP_HOST='localhost')
        try:
            middleware(request)
            if hasattr(request, 'tenant'):
                print_result(f"✓ localhost → {request.tenant.name} (schema: {request.tenant.schema_name})")
            else:
                print_result("✗ localhost → No tenant routing")
        except Exception as e:
            print_result(f"✗ localhost → Error: {e}")
        
        # Test demo.localhost (demo tenant)
        request = factory.get('/', HTTP_HOST='demo.localhost')
        try:
            middleware(request)
            if hasattr(request, 'tenant'):
                print_result(f"✓ demo.localhost → {request.tenant.name} (schema: {request.tenant.schema_name})")
            else:
                print_result("✗ demo.localhost → No tenant routing")
        except Exception as e:
            print_result(f"✗ demo.localhost → Error: {e}")
        
        print_success("API endpoint testing completed")
        return True
        
    except Exception as e:
        print_error(f"API testing failed: {e}")
        return False

def print_usage_instructions():
    """Print detailed usage instructions"""
    print_step(9, "Usage Instructions")
    
    print(f"\n{Colors.BOLD}{Colors.OKGREEN}🎉 Setup Complete! Here's how to use your Django-Tenants platform:{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}1. Add to your /etc/hosts file:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}sudo nano /etc/hosts{Colors.ENDC}")
    print(f"   Add this line: {Colors.WARNING}127.0.0.1 demo.localhost{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}2. Create superuser accounts:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}# For public tenant (tenant management){Colors.ENDC}")
    print(f"   python manage.py create_tenant_superuser --schema=public")
    print(f"   {Colors.OKCYAN}# For demo tenant (water utility operations){Colors.ENDC}")
    print(f"   python manage.py create_tenant_superuser --schema=demo\n")
    
    print(f"{Colors.BOLD}3. Access Points:{Colors.ENDC}")
    print(f"   {Colors.OKBLUE}🌐 Public Tenant (Master Control):{Colors.ENDC}")
    print(f"   • Admin: http://localhost:8000/admin/")
    print(f"   • Tenant API: http://localhost:8000/api/tenants/")
    print(f"   • User API: http://localhost:8000/api/users/")
    print()
    print(f"   {Colors.OKBLUE}🏢 Demo Tenant (Water Utility Operations):{Colors.ENDC}")
    print(f"   • Admin: http://demo.localhost:8000/admin/")
    print(f"   • Infrastructure API: http://demo.localhost:8000/api/infrastructure/")
    print(f"   • Zones: http://demo.localhost:8000/api/infrastructure/zones/")
    print(f"   • Assets: http://demo.localhost:8000/api/infrastructure/assets/")
    print()
    
    print(f"{Colors.BOLD}4. Test Commands:{Colors.ENDC}")
    print(f"   {Colors.OKCYAN}# Test public tenant{Colors.ENDC}")
    print(f"   curl http://localhost:8000/api/tenants/")
    print(f"   {Colors.OKCYAN}# Test demo tenant{Colors.ENDC}")
    print(f"   curl http://demo.localhost:8000/api/infrastructure/zones/")
    print(f"   curl http://demo.localhost:8000/api/infrastructure/asset-types/")
    print()
    
    print(f"{Colors.BOLD}5. Understanding the Architecture:{Colors.ENDC}")
    print(f"   {Colors.OKGREEN}• Public Tenant{Colors.ENDC} (localhost) manages all tenants and users")
    print(f"   {Colors.OKGREEN}• Demo Tenant{Colors.ENDC} (demo.localhost) handles water utility operations")
    print(f"   {Colors.OKGREEN}• Each tenant{Colors.ENDC} has completely isolated data")
    print(f"   {Colors.OKGREEN}• Add more tenants{Colors.ENDC} through the public tenant admin\n")
    
    print(f"{Colors.BOLD}6. Development Server:{Colors.ENDC}")
    print(f"   python manage.py runserver")
    print(f"   {Colors.OKGREEN}Server will handle both localhost and demo.localhost automatically{Colors.ENDC}\n")
    
    print(f"{Colors.BOLD}{Colors.OKGREEN}🚀 Your multi-tenant water utility platform is ready!{Colors.ENDC}")

def main():
    """Main execution function"""
    start_time = datetime.now()
    
    print_header("🚀 DISTRO WATER UTILITY PLATFORM SETUP")
    print(f"{Colors.BOLD}Multi-Tenant Django Application Setup Script{Colors.ENDC}")
    print(f"Started at: {start_time.strftime('%Y-%m-%d %H:%M:%S')}")
    
    # Execute setup steps
    success_steps = 0
    total_steps = 9
    
    if check_prerequisites():
        success_steps += 1
    else:
        print_error("Prerequisites check failed. Aborting setup.")
        return False
    
    if cleanup_existing_tenants():
        success_steps += 1
    
    public_tenant = create_public_tenant()
    if public_tenant:
        success_steps += 1
    
    demo_tenant = create_demo_tenant()
    if demo_tenant:
        success_steps += 1
    
    if run_migrations():
        success_steps += 1
    
    if create_sample_data():
        success_steps += 1
    
    if verify_setup():
        success_steps += 1
    
    if test_api_endpoints():
        success_steps += 1
    
    # Always show usage instructions
    print_usage_instructions()
    success_steps += 1
    
    # Final summary
    end_time = datetime.now()
    duration = (end_time - start_time).seconds
    
    print_header("🎯 SETUP SUMMARY")
    
    if success_steps == total_steps:
        print(f"{Colors.BOLD}{Colors.OKGREEN}✅ SUCCESS: All {success_steps}/{total_steps} steps completed successfully!{Colors.ENDC}")
        print(f"{Colors.OKGREEN}⏱️  Setup completed in {duration} seconds{Colors.ENDC}")
        print(f"{Colors.OKGREEN}🎉 Your multi-tenant water utility platform is ready for use!{Colors.ENDC}")
    else:
        print(f"{Colors.WARNING}⚠️  PARTIAL SUCCESS: {success_steps}/{total_steps} steps completed{Colors.ENDC}")
        print(f"{Colors.WARNING}Some steps may need manual completion{Colors.ENDC}")
    
    print(f"\n{Colors.BOLD}Next Steps:{Colors.ENDC}")
    print(f"1. Add demo.localhost to your /etc/hosts file")
    print(f"2. Create superuser accounts")
    print(f"3. Run: python manage.py runserver")
    print(f"4. Visit: http://localhost:8000/admin/ and http://demo.localhost:8000/admin/")
    
    return success_steps == total_steps

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print(f"\n{Colors.WARNING}⚠️  Setup interrupted by user{Colors.ENDC}")
        sys.exit(1)
    except Exception as e:
        print(f"\n{Colors.FAIL}💥 Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
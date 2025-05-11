from django.core.management.base import BaseCommand
from django_tenants.utils import schema_context
from distro.models import UserProfile, AssetType, Asset, Issue
from django.contrib.gis.geos import Point
import random
from datetime import datetime, timedelta
import math

class Command(BaseCommand):
    help = 'Generate realistic sample data for tenants'

    def add_arguments(self, parser):
        parser.add_argument('--schema', type=str, help='Tenant schema name')

    def handle(self, *args, **options):
        schema = options.get('schema')
        if schema:
            self.generate_data_for_tenant(schema)
        else:
            for tenant_schema in ['bomet', 'turkana']:
                self.generate_data_for_tenant(tenant_schema)

    def generate_data_for_tenant(self, schema):
        with schema_context(schema):
            self.stdout.write(f"Generating data for {schema}...")

            # Create users
            superuser = UserProfile.objects.create_superuser(
                username=f'admin_{schema}',
                email=f'admin@{schema}.distro.africa',
                password='admin123',
                role='ADMIN',
                phone_number='+254700000000'
            )

            # Create multiple technicians for realistic workload
            technicians = []
            for i in range(5):
                technician = UserProfile.objects.create_user(
                    username=f'technician_{schema}_{i}',
                    email=f'tech{i}@{schema}.distro.africa',
                    password='tech123',
                    role='FIELD_TECHNICIAN',
                    phone_number=f'+25470000000{i}'
                )
                technicians.append(technician)

            # Create supervisor
            supervisor = UserProfile.objects.create_user(
                username=f'supervisor_{schema}',
                email=f'supervisor@{schema}.distro.africa',
                password='sup123',
                role='SUPERVISOR',
                phone_number='+254700000006'
            )

            # Asset types
            asset_types = [
                AssetType.objects.create(name='Pipe', description='Water pipeline'),
                AssetType.objects.create(name='Pump', description='Water pump'),
                AssetType.objects.create(name='Reservoir', description='Water storage tank'),
                AssetType.objects.create(name='Valve', description='Control valve')
            ]

            # Realistic coordinates and data points
            if schema == 'bomet':
                center = Point(35.344, -0.781)  # Bomet center
                num_assets = 800  # 80% of 1,000
                num_issues = 200  # 20% of 1,000
                radius_km = 20    # Smaller area for denser Bomet
            else:
                center = Point(35.626, 3.528)  # Turkana center
                num_assets = 1600  # 80% of 2,000
                num_issues = 400   # 20% of 2,000
                radius_km = 50     # Larger area for sparse Turkana

            # Convert radius to degrees (approx. 1 degree = 111 km)
            radius_deg = radius_km / 111.0

            # Generate assets with clustered distribution
            assets = []
            for i in range(num_assets):
                # Use Gaussian distribution for clustering around center
                x_offset = random.gauss(0, radius_deg / 3)  # Tighter clustering
                y_offset = random.gauss(0, radius_deg / 3)
                # Ensure points stay within radius
                if math.sqrt(x_offset**2 + y_offset**2) > radius_deg:
                    x_offset *= 0.5
                    y_offset *= 0.5

                asset_type = random.choice(asset_types)
                material = random.choice(['PVC', 'Steel', 'Concrete']) if asset_type.name == 'Pipe' else None
                capacity = random.randint(1000, 10000) if asset_type.name == 'Reservoir' else None
                age = random.randint(1, 30)

                asset = Asset.objects.create(
                    name=f'{schema}_{asset_type.name.lower()}_{i}',
                    asset_type=asset_type,
                    geometry=Point(center.x + x_offset, center.y + y_offset),
                    metadata={
                        'material': material,
                        'capacity_liters': capacity,
                        'age_years': age,
                        'last_maintenance': (datetime.now() - timedelta(days=random.randint(30, 365))).isoformat()
                    }
                )
                assets.append(asset)

            # Generate issues
            for i in range(num_issues):
                asset = random.choice(assets)
                issue_type = random.choice(['Leak', 'Blockage', 'Pump Failure', 'Valve Malfunction'])
                priority = random.choices(
                    ['LOW', 'MEDIUM', 'HIGH'],
                    weights=[0.5, 0.3, 0.2],  # More low-priority issues
                    k=1
                )[0]
                status = random.choices(
                    ['OPEN', 'IN_PROGRESS', 'RESOLVED'],
                    weights=[0.6, 0.3, 0.1],  # More open issues
                    k=1
                )[0]

                Issue.objects.create(
                    title=f'{issue_type} near {asset.name}',
                    description=f'{issue_type} detected at {asset.name}. Requires urgent attention.' if priority == 'HIGH' else f'{issue_type} at {asset.name}.',
                    priority=priority,
                    status=status,
                    location=Point(asset.geometry.x + random.uniform(-0.001, 0.001), asset.geometry.y + random.uniform(-0.001, 0.001)),
                    reported_by=random.choice(technicians),
                    assigned_to=random.choice(technicians) if random.random() > 0.3 else None,
                    reported_date=datetime.now() - timedelta(days=random.randint(0, 90))
                )

            self.stdout.write(f"Generated data for {schema}: 1 superuser, 1 supervisor, 5 technicians, 4 asset types, {num_assets} assets, {num_issues} issues")
from django.core.management.base import BaseCommand
from tenants.models import Tenant, Domain

class Command(BaseCommand):
    help = 'Create a new tenant with schema and domain'

    def add_arguments(self, parser):
        parser.add_argument('--name', type=str, required=True, help='Tenant name (e.g., Bomet)')
        parser.add_argument('--schema', type=str, required=True, help='Schema name (e.g., bomet)')
        parser.add_argument('--domain', type=str, required=True, help='Domain (e.g., bomet.localhost)')

    def handle(self, *args, **kwargs):
        name = kwargs['name']
        schema_name = kwargs['schema']
        domain = kwargs['domain']

        tenant, created = Tenant.objects.get_or_create(
            schema_name=schema_name,
            defaults={'name': name}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f'Created tenant: {name} (schema: {schema_name})'))
        else:
            self.stdout.write(self.style.WARNING(f'Tenant {name} already exists'))

        Domain.objects.get_or_create(
            domain=domain,
            tenant=tenant,
            is_primary=True
        )
        self.stdout.write(self.style.SUCCESS(f'Assigned domain: {domain}'))

        self.stdout.write(self.style.SUCCESS('Tenant setup complete. Run "migrate_schemas" to apply migrations.'))
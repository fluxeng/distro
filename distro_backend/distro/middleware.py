from django_tenants.utils import get_tenant_model, schema_context

class TenantHeaderMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        tenant_schema = request.headers.get('X-Tenant-Schema')
        if tenant_schema:
            Tenant = get_tenant_model()
            try:
                tenant = Tenant.objects.get(schema_name=tenant_schema)
                with schema_context(tenant.schema_name):
                    response = self.get_response(request)
                return response
            except Tenant.DoesNotExist:
                pass
        return self.get_response(request)
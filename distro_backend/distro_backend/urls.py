from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse
from django_tenants.middleware import TenantMainMiddleware  # Correct import

# Public schema URLs
def health_check(request):
    """Simple health check endpoint"""
    return JsonResponse({'status': 'healthy', 'version': '1.0'})

def tenant_info(request):
    """Public endpoint to show available tenants"""
    return JsonResponse({
        'message': 'Distro V1 - Water Utility Management Platform',
        'version': '1.0',
        'documentation': '/api/docs/'
    })

public_urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('health/', health_check, name='health_check'),
    path('', tenant_info, name='tenant_info'),
    path('api/auth/', include('rest_framework.urls')),
]

# Tenant-specific URLs
tenant_urlpatterns = [
    path('admin/', admin.site.urls, name='tenant_admin'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/tenants/', include('tenants.urls')),
    path('api/utilities/', include('utilities.urls')),
    path('api/infrastructure/', include('infrastructure.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/customer-support/', include('customer_support.urls')),
]

# Main URL patterns
urlpatterns = public_urlpatterns + tenant_urlpatterns

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
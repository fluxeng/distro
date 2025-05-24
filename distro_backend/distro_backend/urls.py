from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.http import JsonResponse

# Public schema URLs
def health_check(request):
    return JsonResponse({'status': 'healthy', 'version': '1.0'})

def tenant_info(request):
    return JsonResponse({
        'message': 'Distro V1 - Water Utility Management Platform',
        'version': '1.0',
        'documentation': '/api/docs/'
    })

urlpatterns = [
    # Shared
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('health/', health_check),
    path('', tenant_info),

    # Tenant-specific APIs
    path('api/tenants/', include('tenants.urls')),
    path('api/utilities/', include('utilities.urls')),
    path('api/infrastructure/', include('infrastructure.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/customer-support/', include('customer_support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

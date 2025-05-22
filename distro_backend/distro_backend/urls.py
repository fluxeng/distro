# distro_backend/urls.py (Main tenant URLs)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/', include('rest_framework.urls')),
    path('api/utilities/', include('utilities.urls')),
    path('api/infrastructure/', include('infrastructure.urls')),
    path('api/maintenance/', include('maintenance.urls')),
    path('api/customer-support/', include('customer_support.urls')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)


# distro_backend/urls_public.py (Public schema URLs)
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse

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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('health/', health_check, name='health_check'),
    path('', tenant_info, name='tenant_info'),
]
from django.contrib import admin
from django.urls import path
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
"""
Single URL configuration for both public and tenant schemas
Django-tenants will automatically handle which apps are available in which schema
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import (
    SpectacularAPIView, 
    SpectacularRedocView, 
    SpectacularSwaggerView
)

urlpatterns = [
    # Admin interface
    path('admin/', admin.site.urls),
    
    # API Documentation
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
    
    # All APIs - django-tenants handles which work where
    path('api/tenants/', include('tenants.urls')),      # Only works in public schema
    path('api/users/', include('users.urls')),          # Works in both schemas  
    path('api/infrastructure/', include('infrastructure.urls')),  # Only works in tenant schemas
    
    # DRF Auth (for API browsing)
    path('api-auth/', include('rest_framework.urls')),
    
    # Health check with schema info
    path('health/', lambda request: __import__('django.http').HttpResponse(
        f'OK - Schema: {getattr(getattr(request, "tenant", None), "schema_name", "public")}'
    )),
    
    # Root redirect to API docs
    path('', lambda request: __import__('django.shortcuts').redirect('/api/docs/')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

# Dynamic admin configuration based on current schema
def configure_admin():
    try:
        from django.db import connection
        if hasattr(connection, 'schema_name'):
            if connection.schema_name == 'public':
                admin.site.site_header = "Distro V1 Master Control"
                admin.site.site_title = "Multi-Tenant Management"
                admin.site.index_title = "Tenant & User Administration"
            else:
                admin.site.site_header = "Water Utility Administration"
                admin.site.site_title = "Infrastructure Management"  
                admin.site.index_title = "Assets & Operations"
    except:
        # Fallback configuration
        admin.site.site_header = "Distro V1 Administration"
        admin.site.site_title = "Distro V1 Admin"

configure_admin()
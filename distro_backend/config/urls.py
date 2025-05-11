from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.conf import settings
from django.conf.urls.static import static

def health_check(request):
    return HttpResponse("OK", status=200)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('distro.urls')),
    path('api/health/', health_check, name='health_check'),
]

# Only add media URL patterns for development
# WhiteNoise automatically handles static files in both development and production
if settings.DEBUG:
    # Serve media files in development
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
    # Optional: You can also add static files for development if needed
    # but WhiteNoise will handle them anyway
    # urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

# Note: No need to add static files URL patterns because:
# 1. WhiteNoise middleware handles static files automatically
# 2. It works at the WSGI level, before URL routing
# 3. It's compatible with django-tenants multi-tenancy
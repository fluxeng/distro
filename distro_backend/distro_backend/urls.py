# distro_backend/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tenants/', include('tenants.urls', namespace='tenants')),
    path('api-auth/', include('rest_framework.urls')),  # Optional: for DRF login/logout
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/tenants/', include('tenants.urls')),
    path('api/users/', include('users.urls')),  # Add this line
    path('api-auth/', include('rest_framework.urls')),
    path('api/infrastructure/', include('infrastructure.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
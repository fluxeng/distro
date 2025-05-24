from django.urls import path
from django.contrib import admin
from . import views

app_name = 'tenants'

urlpatterns = [
    # Tenant management endpoints
    path('api/tenants/create/', views.create_tenant_api, name='create_tenant'),
    path('api/tenants/<int:utility_id>/delete/', views.delete_tenant_api, name='delete_tenant'),  # soft delete
    path('api/tenants/<int:utility_id>/restore/', views.restore_tenant_api, name='restore_tenant'),
    path('api/tenants/<int:utility_id>/permanent-delete/', views.permanently_delete_tenant_api, name='permanently_delete_tenant'),
    path('api/tenants/<int:utility_id>/toggle/', views.toggle_tenant_status_api, name='toggle_tenant_status'),
    path('api/tenants/<int:utility_id>/', views.get_tenant_info_api, name='get_tenant_info'),
    path('api/tenants/', views.list_tenants_api, name='list_tenants'),
    
    # Domain management endpoints
    path('api/tenants/<int:utility_id>/domains/', views.add_domain_api, name='add_domain'),
]
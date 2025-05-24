from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.core.exceptions import ValidationError
import json
import logging
from .utils import (
    create_tenant, soft_delete_tenant, restore_tenant, permanently_delete_tenant,
    add_domain_to_tenant, toggle_tenant_status, list_tenants, get_tenant_info
)

logger = logging.getLogger('tenants')


@csrf_exempt
@require_http_methods(["POST"])
def create_tenant_api(request):
    """
    API endpoint to create a new tenant
    
    POST /api/tenants/create/
    {
        "name": "Nairobi Water Company",
        "domain": "nairobi.distro.app"
    }
    """
    try:
        data = json.loads(request.body)
        name = data.get('name')
        domain_name = data.get('domain')
        
        if not name or not domain_name:
            return JsonResponse({
                'success': False,
                'error': 'Both name and domain are required'
            }, status=400)
        
        utility, domain = create_tenant(name, domain_name)
        
        return JsonResponse({
            'success': True,
            'data': {
                'utility_id': utility.id,
                'name': utility.name,
                'schema_name': utility.schema_name,
                'domain': domain.domain,
                'is_primary': domain.is_primary
            }
        })
        
    except ValidationError as e:
        logger.error(f"Validation error in create_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except json.JSONDecodeError:
        return JsonResponse({
            'success': False,
            'error': 'Invalid JSON data'
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in create_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def soft_delete_tenant_api(request, utility_id):
    """
    API endpoint to soft delete a tenant
    
    DELETE /api/tenants/{utility_id}/delete/
    {
        "confirm_name": "Nairobi Water Company"
    }
    """
    try:
        data = json.loads(request.body) if request.body else {}
        confirm_name = data.get('confirm_name')
        
        utility = soft_delete_tenant(utility_id, confirm_name)
        
        return JsonResponse({
            'success': True,
            'message': 'Tenant soft deleted successfully',
            'data': {
                'utility_id': utility.id,
                'name': utility.name,
                'is_deleted': utility.is_deleted,
                'deleted_on': utility.deleted_on.isoformat() if utility.deleted_on else None
            }
        })
        
    except ValidationError as e:
        logger.error(f"Validation error in soft_delete_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in soft_delete_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["POST"])
def restore_tenant_api(request, utility_id):
    """
    API endpoint to restore a soft-deleted tenant
    
    POST /api/tenants/{utility_id}/restore/
    """
    try:
        utility = restore_tenant(utility_id)
        
        return JsonResponse({
            'success': True,
            'message': 'Tenant restored successfully',
            'data': {
                'utility_id': utility.id,
                'name': utility.name,
                'is_active': utility.is_active,
                'is_deleted': utility.is_deleted
            }
        })
        
    except ValidationError as e:
        logger.error(f"Validation error in restore_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in restore_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def permanently_delete_tenant_api(request, utility_id):
    """
    API endpoint to permanently delete a tenant (only works on soft-deleted tenants)
    
    DELETE /api/tenants/{utility_id}/permanent-delete/
    {
        "confirm_name": "Nairobi Water Company"
    }
    """
    try:
        data = json.loads(request.body) if request.body else {}
        confirm_name = data.get('confirm_name')
        
        success = permanently_delete_tenant(utility_id, confirm_name)
        
        return JsonResponse({
            'success': success,
            'message': 'Tenant permanently deleted successfully'
        })
        
    except ValidationError as e:
        logger.error(f"Validation error in permanently_delete_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in permanently_delete_tenant_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_tenant_api(request, utility_id):
    """
    API endpoint to soft delete a tenant (backward compatibility)
    
    DELETE /api/tenants/{utility_id}/delete/
    {
        "confirm_name": "Nairobi Water Company"
    }
    """
    return soft_delete_tenant_api(request, utility_id)


@csrf_exempt
@require_http_methods(["POST"])
def add_domain_api(request, utility_id):
    """
    API endpoint to add a domain to existing tenant
    
    POST /api/tenants/{utility_id}/domains/
    {
        "domain": "new-domain.com",
        "is_primary": false
    }
    """
    try:
        data = json.loads(request.body)
        domain_name = data.get('domain')
        is_primary = data.get('is_primary', False)
        
        if not domain_name:
            return JsonResponse({
                'success': False,
                'error': 'Domain name is required'
            }, status=400)
        
        domain = add_domain_to_tenant(utility_id, domain_name, is_primary)
        
        return JsonResponse({
            'success': True,
            'data': {
                'domain': domain.domain,
                'is_primary': domain.is_primary,
                'is_active': domain.is_active
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in add_domain_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@csrf_exempt
@require_http_methods(["PATCH"])
def toggle_tenant_status_api(request, utility_id):
    """
    API endpoint to toggle tenant active status
    
    PATCH /api/tenants/{utility_id}/toggle/
    {
        "is_active": true  // optional, will toggle if not provided
    }
    """
    try:
        data = json.loads(request.body) if request.body else {}
        is_active = data.get('is_active')
        
        utility = toggle_tenant_status(utility_id, is_active)
        
        return JsonResponse({
            'success': True,
            'data': {
                'utility_id': utility.id,
                'name': utility.name,
                'is_active': utility.is_active
            }
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=400)
    except Exception as e:
        logger.error(f"Unexpected error in toggle_tenant_status_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def list_tenants_api(request):
    """
    API endpoint to list all tenants
    
    GET /api/tenants/?active_only=true&include_deleted=false
    """
    try:
        active_only = request.GET.get('active_only', 'false').lower() == 'true'
        include_deleted = request.GET.get('include_deleted', 'false').lower() == 'true'
        tenants = list_tenants(active_only, include_deleted)
        
        data = []
        for tenant in tenants:
            tenant_data = {
                'id': tenant.id,
                'name': tenant.name,
                'schema_name': tenant.schema_name,
                'is_active': tenant.is_active,
                'is_deleted': tenant.is_deleted,
                'deleted_on': tenant.deleted_on.isoformat() if tenant.deleted_on else None,
                'created_on': tenant.created_on.isoformat(),
                'domains': [
                    {
                        'domain': domain.domain,
                        'is_primary': domain.is_primary,
                        'is_active': domain.is_active
                    }
                    for domain in tenant.domains.all()
                ]
            }
            data.append(tenant_data)
        
        return JsonResponse({
            'success': True,
            'data': data,
            'count': len(data)
        })
        
    except Exception as e:
        logger.error(f"Unexpected error in list_tenants_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)


@require_http_methods(["GET"])
def get_tenant_info_api(request, utility_id):
    """
    API endpoint to get detailed tenant information
    
    GET /api/tenants/{utility_id}/
    """
    try:
        info = get_tenant_info(utility_id)
        
        return JsonResponse({
            'success': True,
            'data': info
        })
        
    except ValidationError as e:
        return JsonResponse({
            'success': False,
            'error': str(e)
        }, status=404)
    except Exception as e:
        logger.error(f"Unexpected error in get_tenant_info_api: {str(e)}")
        return JsonResponse({
            'success': False,
            'error': 'Internal server error'
        }, status=500)
from rest_framework import permissions

class IsAdminOrSupervisor(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role in ['ADMIN', 'SUPERVISOR']

class IsFieldTechnician(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'FIELD_TECHNICIAN'
from rest_framework.permissions import BasePermission

class IsGlobalSuperAdmin(BasePermission):
    """
    Allows access only to global superadmins (no tenant association).
    """
    def has_permission(self, request, view):
        user = request.user
        return user.is_authenticated and user.is_superuser and user.tenant is None

from rest_framework.permissions import BasePermission
    
class IsSuperUserOrAuthenticatedUser(BasePermission):
    """
    - Superusers can access objects not owned by other superuser
    - Authenticated non-superusers can access only their own objects
    """
    def has_permission(self, request, view):
        return request.user and request.user.is_authenticated
    
    def has_object_permission(self, request, view, obj):
        if request.user.is_superuser:
            return not obj.owner.is_superuser
        return obj.owner == request.user

from rest_framework import permissions

class IsSuperUser(permissions.BasePermission):
    """
        Custom permission to allow superusers to perform CRUD on all non-superuser objects,
        and non-superusers to perform CRUD only on their own objects.
    """
    def has_permission(self, request, view):
        return bool(
            request.user and request.user.is_authenticated and request.user.is_superuser
        )

class IsSuperUserOrOwner(permissions.BasePermission):
    """
    Allow superusers full access to non-superuser-owned objects,
    and regular users to access only their own.
    """
    def has_object_permission(self, request, view, obj):
        # Superuser can access if the target is not owned by another superuser
        if request.user.is_superuser:
            return not obj.owner.is_superuser

        # Non-superusers can only access their own objects
        return obj.owner == request.user
    
class IsOwner(permissions.BasePermission):
    """
    Grants access only to the object's owner.
    """
    def has_object_permission(self, request, view, obj):
        return obj.owner == request.user
    
class IsAuthenticatedAndNotSuperUser(permissions.BasePermission):
    """
    Allow only authenticated users who are not superusers.
    """
    def has_permission(self, request, view):
        return (
            request.user and request.user.is_authenticated and not request.user.is_superuser
        )
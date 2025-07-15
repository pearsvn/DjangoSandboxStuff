from rest_framework.permissions import BasePermission
    

SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

class SuperUserAccessPemission(BasePermission):
    
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return True
        else:
            return request.user.is_superuser
from rest_framework.permissions import BasePermission

class IsParentOrAdmin(BasePermission):    
    def has_permission(self, request, view):
        return request.user.role in ['Parent', 'Admin']


class IsOwnerOrAdmin(BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.user.role == 'Admin':
            return True
        if request.user.role == 'Parent':
            return obj.parent == request.user
        if request.user.role == 'Kid':
            return obj.kid == request.user
        return False

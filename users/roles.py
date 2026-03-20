from rest_framework.permissions import BasePermission

class IsTrainer(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainer'
    
class IsTrainee(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'trainee'
    
class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.role == 'admin'
    
class IsAdminOrTrainer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated and
            request.user.role in ['admin', 'trainer']
        )
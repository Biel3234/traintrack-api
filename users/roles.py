from rest_framework.permissions import BasePermission

class IsTrainer(BasePermission):
    def has_permission(self, request, user, view):
        return request.user.role == 'trainer'
    
class IsTrainee(BasePermission):
    def has_permission(self, request, user, view):
        return request.user.role == 'trainee'
    
class IsAdmin(BasePermission):
    def has_permission(self, request, user, view):
        return request.user.role == 'admin'
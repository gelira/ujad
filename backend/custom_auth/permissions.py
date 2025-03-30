from rest_framework.permissions import BasePermission

from custom_auth.models import User

def check_user(user):
    return bool(user and user.is_active)

class IsAuthenticatedAndActivePermission(BasePermission):
    def has_permission(self, request, view):
        return check_user(request.user)
    
class IsConsumerAuthenticatedAndActivePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return check_user(user) and user.role == User.ROLE_CONSUMER
    
class IsDispatcherAuthenticatedAndActivePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return check_user(user) and user.role == User.ROLE_DISPATCHER

class IsAdminAuthenticatedAndActivePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        return check_user(user) and user.role == User.ROLE_ADMIN

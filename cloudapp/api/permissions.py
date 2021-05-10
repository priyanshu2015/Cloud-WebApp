from rest_framework import permissions
from ..models import User
class IsRootUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if  user.type == User.Types.Root:
            return True
        else:
            return False
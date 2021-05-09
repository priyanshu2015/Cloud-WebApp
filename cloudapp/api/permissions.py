from rest_framework import permissions
class IsRootUser(permissions.BasePermission):
    def has_permission(self, request, view):
        user = request.user
        if  user.type == User.Types.Root:
            return True
        else:
            return False
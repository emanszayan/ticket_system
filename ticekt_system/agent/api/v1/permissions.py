from rest_framework import permissions


class OwnProfileOrAdminPermission(permissions.BasePermission):
    """
    Object-level permission to only allow updating his own profile
    """

    def has_object_permission(self, request, view, user):
        # Always return True if superuser
        if request.user.is_superuser:
            return True

        # obj here is a UserProfile instance
        return user == request.user


class IsStaffUser(permissions.BasePermission):
    """
    Check if request user is staff user
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_staff)


class IsSuperUser(permissions.BasePermission):
    """
    Check if request user is Super user
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_superuser)


class IsAgent(permissions.BasePermission):
    """
    Check if request user is agent
    """

    def has_permission(self, request, view):
        return bool(request.user and request.user.is_agent)


class UserDjangoModelPermissions(permissions.DjangoModelPermissions):
    """
    user model permission for curd operation
    """
    perms_map = {
        'GET': ['account.view_user'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': [],
        'PUT': ['account.change_user'],
        'PATCH': ['account.change_user'],
        'DELETE': ['account.delete_user'],
    }


class PermissionDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['auth.view_permission'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['auth.add_permission'],
        'PUT': ['auth.change_permission'],
        'PATCH': ['auth.change_permission'],
        'DELETE': ['auth.delete_permission'],
    }


class GroupDjangoModelPermissions(permissions.DjangoModelPermissions):
    perms_map = {
        'GET': ['auth.view_group'],
        'OPTIONS': [],
        'HEAD': [],
        'POST': ['auth.add_group'],
        'PUT': ['auth.change_group'],
        'PATCH': ['auth.change_group'],
        'DELETE': ['auth.delete_group'],
    }

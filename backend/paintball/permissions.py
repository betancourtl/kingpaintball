from rest_framework import permissions


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        is_read_only = bool(
            # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            request.method in permissions.SAFE_METHODS
        )

        print(f'is_read_only: {is_read_only}')
        return is_read_only


class IsAdmin(permissions.BasePermission):
    """The request is authenticated as an admin, or is a read-only request"""

    def has_permission(self, request, view):
        is_admin = bool(request.user and request.user.is_staff)

        print(f'is_admin: {is_admin}')
        return is_admin


class IsOwner(permissions.BasePermission):
    """
    Object-level permission to only allow owners of an object to edit it.
    Assumes the model instance has an `owner` attribute.
    """

    def has_object_permission(self, request, view, obj):
    
        # Instance must have an attribute named `owner`.
        print('Object Permission')
        return obj.owner == request.user

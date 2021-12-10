from rest_framework import permissions
SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')

# authentication -> populates user and token
# permissions
# controller
# model
# db

# This only runs on urls that have the following pattern /api/some-path/<id>/
# If will get you the object by it's id.
class IsOwnerOrReadOnly(permissions.BasePermission):
    # This runs on: # GET, PUT, PATCH , DELETE
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTION
        if request.method in SAFE_METHODS:
            return True

        # POST, PUT, PATCH, DELETE
        is_object_owner = obj.user == request.user
        return is_object_owner


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        is_read_only = bool(
            # SAFE_METHODS = ('GET', 'HEAD', 'OPTIONS')
            request.method in permissions.SAFE_METHODS
        )

        return is_read_only

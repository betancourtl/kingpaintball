from rest_framework import permissions


# This only runs on urls that have the following pattern /api/some-path/<id>/
# If will get you the object by it's id.

class IsOwnerOrReadOnly(permissions.BasePermission):
    # This runs on: # GET, PUT, PATCH , DELETE
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTION
        if request.method in permissions.SAFE_METHODS:
            return True

        # PUT, PATCH, DELETE
        is_object_owner = obj.user == request.user
        return is_object_owner


class IsImageOwnerOrReadOnly(permissions.BasePermission):
    # This runs on: # GET, PUT, PATCH , DELETE
    def has_object_permission(self, request, view, obj):
        # GET, HEAD, OPTION
        if request.method in permissions.SAFE_METHODS:
            return True

        # PUT, PATCH, DELETE
        is_object_owner = obj.item.user == request.user
        return is_object_owner


class IsReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        is_read_only = bool(
            request.method in permissions.SAFE_METHODS
        )

        return is_read_only

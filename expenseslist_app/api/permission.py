from rest_framework import permissions


class IsAdminOrReadOnly(permissions.IsAdminUser):
    def has_permision(self, request, view):
        if request.method == "GET":
            return True

        staff_permission = bool(request.user and request.user.is_staff)
        return staff_permission


class IsRecordUserOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return obj.created_by == request.user or request.user.is_staff

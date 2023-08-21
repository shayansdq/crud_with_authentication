from rest_framework.permissions import BasePermission, SAFE_METHODS
from rest_framework.request import Request


class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        return request.user.id == obj.user.id

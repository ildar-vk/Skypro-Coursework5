from rest_framework.permissions import BasePermission


class IsOwnerOrReadOnly(BasePermission):
    """Пользователь может редактировать только свои привычки."""

    def has_object_permission(self, request, view, obj):
        if request.method in ('GET', 'HEAD', 'OPTIONS'):
            return obj.is_public or obj.user == request.user
        return obj.user == request.user
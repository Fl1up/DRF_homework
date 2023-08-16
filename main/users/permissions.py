from rest_framework.permissions import BasePermission


class IsOwnerOrModerator(BasePermission):
    """Проверка прав доступа - Владелец или Модератор"""

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator").exists():
            return True

        return request.user == view.get_object().owner


class IsNotModerator(BasePermission):
    """Проверка прав доступа НЕ МОДЕРАТОР"""

    def has_permission(self, request, view):
        if request.user.groups.filter(name="Moderator").exists():
            return False

        return True


class IsOwner(BasePermission):
    """Проверка прав доступа ПОЛЬЗОВАТЕЛЬ"""

    def has_permission(self, request, view):
        return request.user == view.get_object().owner

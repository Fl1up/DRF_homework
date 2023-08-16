from rest_framework.permissions import BasePermission


class IsOwnerOrStaff(BasePermission):  # Создание функции для авторизации. Если не стаф и не владелец редактирование запрещено

    def has_permission(self, request, view):
        if request.user.is_staff:
            return True
        return request.user == view.get_object.owner
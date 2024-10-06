from rest_framework import permissions


class IsAuthorOrReadOnly(permissions.BasePermission):
    """
    Разрешение только для автора объекта. Другие пользователи могут только просматривать объект.
    """

    def has_object_permission(self, request, view, obj):
        # Разрешаем только безопасные методы (GET, HEAD или OPTIONS)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Проверяем, является ли пользователь автором объекта
        return obj.author == request.user
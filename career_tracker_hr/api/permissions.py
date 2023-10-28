from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAuthorOrHRReadOnly(BasePermission):
    """Редактирование разрешено только автору,
    просмотр только пользователям с ролью HR"""
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            return request.user.role == 'HR'
        return (obj.author == request.user
                or request.user.is_superuser)
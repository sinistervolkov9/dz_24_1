from rest_framework.permissions import BasePermission


# class IsModer(BasePermission):
#     def has_permission(self, request, view):
#         print(request.method)
#         return request.user.groups.filter(name='Модератор').exists() and request.method not in ['DELETE', 'POST']
#
#
# class IsAuthorOrReadOnly(BasePermission):
#     def has_object_permission(self, request, view, obj):
#         if request.method in ['GET', 'HEAD', 'OPTIONS']:
#             return True
#         return obj.user == request.user

class IsModerOrAuthor(BasePermission):
    def has_permission(self, request, view):
        if request.user.groups.filter(name='Модератор').exists():
            if request.method in ['DELETE', 'POST']:
                return False
            return True

        return request.method in SAFE_METHODS or request.user.is_authenticated

    def has_object_permission(self, request, view, obj):
        if request.user.groups.filter(name='Модератор').exists():
            if request.method in ['DELETE', 'POST']:
                return False
            return True

        return obj.author == request.user or request.method in SAFE_METHODS

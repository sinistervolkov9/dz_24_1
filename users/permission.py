from rest_framework.permissions import BasePermission, SAFE_METHODS
from users.models import Payment


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

        return obj.user == request.user or request.method in SAFE_METHODS


class IsPaymet(BasePermission):
    def has_object_permission(self, request, view, obj):
        # return request.user.is_authenticated and obj.payment_course.filter(user=request.user, status='pending').exists()
        return request.user.is_authenticated and obj.payment_course.filter(user=request.user, status=Payment.STATUS_SUCCESS).exists()

from rest_framework.permissions import BasePermission

class IsUser(BasePermission):
    """
    Permission for normal users. Only users can access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'user'


class IsSupervisor(BasePermission):
    """
    Permission for supervisors. Only supervisors can access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'supervisor'


class IsCollector(BasePermission):
    """
    Permission for collectors. Only collectors can access certain views.
    """
    def has_permission(self, request, view):
        return request.user.role == 'collector'

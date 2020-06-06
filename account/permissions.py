from rest_framework import permissions
from account.models import Group, MemeberShip


# 1 User
class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and MemeberShip.objects.filter(group=Group.objects.get(group_name="User"),
                                                       account=request.user):
            return True
        return False


# 2 Staff
class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and MemeberShip.objects.filter(group=Group.objects.get(group_name="Staff"),
                                                       account=request.user):
            return True
        return False


# 3 Manager
class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and MemeberShip.objects.filter(group=Group.objects.get(group_name="Manager"),
                                                       account=request.user):
            return True
        return False


# 4 Administrator
class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and MemeberShip.objects.filter(group=Group.objects.get(group_name="Administrator"),
                                                       account=request.user):
            return True
        return False

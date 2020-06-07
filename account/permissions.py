from rest_framework import permissions
from account.models import Group, MemberShip
from django.contrib.auth.models import AnonymousUser


# from rest_framework

# 1 User
class IsUser(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and \
                MemberShip.objects.filter(group=Group.objects.get(group_name="User"),
                                          account=request.user):
            return True
        return False


# 2 Staff
class IsStaff(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and \
                MemberShip.objects.filter(group=Group.objects.get(group_name="Staff"),
                                          account=request.user):
            return True
        return False


# 3 Manager
class IsManager(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and \
                MemberShip.objects.filter(group=Group.objects.get(group_name="Manager"),
                                          account=request.user):
            return True
        return False


# 4 Administrator
class IsAdministrator(permissions.BasePermission):

    def has_permission(self, request, view):
        if request.user and not request.user.is_anonymous and \
                MemberShip.objects.filter(group=Group.objects.get(group_name="Administrator"),
                                          account=request.user):
            return True
        return False

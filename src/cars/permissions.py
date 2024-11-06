from rest_framework import permissions


class IsAdmin(permissions.BasePermission):


    def has_permission(self, request, view):
        return request.user and request.user.is_staff


class IsEmployee(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == 'employee'


class IsClient(permissions.BasePermission):

    def has_permission(self, request, view):
        return request.user and request.user.role == 'client'

    def has_object_permission(self, request, view, obj):
        # Clients can only view their own car
        return obj.registration_number == request.user.car_registration_number

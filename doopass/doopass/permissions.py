from typing import override
from rest_framework import permissions
from rest_framework.request import Request
from rest_framework import viewsets

from .models import Storage


class IsOwnerPermission(permissions.BasePermission):
    @override
    def has_object_permission(
        self, request: Request, view: viewsets.ModelViewSet, vacation_obj: Storage
    ):
        if request.method in permissions.SAFE_METHODS:
            return True

        if not request.user or not request.user.is_authenticated:
            return False

        if request.method in ["POST"]:
            return True

        if (
            request.method in ["DELETE", "PUT"]
            and vacation_obj.owner.id == request.user.id
        ):

            return True

        return False

from typing import Any, override
from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import generics, viewsets
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny

from .models import Storage, Backup, User
from .modules import password
from .serializers import UserSerializer, StorageSerializer, BackupSerializer
from .permissions import IsOwnerPermission


class BaseUserDataManagementAPIView(APIView):
    def _does_user_password_match(
        self, user: User, request: Request, keyword: str = "password"
    ) -> bool:
        return password.does_password_match(user.password, request.data[keyword])


class UserListAPIView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)


class StorageViewSet(viewsets.ModelViewSet):
    queryset = Storage.objects.all()
    serializer_class = StorageSerializer
    permission_classes = (IsOwnerPermission,)

    def list(self, request: Request, *args, **kwargs) -> Response:
        if "owner_id" in request.query_params:
            serializer = StorageSerializer(
                Storage.objects.filter(owner_id=request.query_params.get("owner_id")),
                many=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)


class BackupViewSet(viewsets.ModelViewSet):
    queryset = Backup.objects.all()
    serializer_class = BackupSerializer
    permission_classes = (IsOwnerPermission,)

    def list(self, request: Request, *args, **kwargs) -> Response:
        if "storage_id" in request.query_params:
            serializer = StorageSerializer(
                Backup.objects.filter(
                    storage_id=request.query_params.get("storage_id")
                ),
                many=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        elif "owner_id" in request.query_params:
            serializer = StorageSerializer(
                Backup.objects.filter(owner_id=request.query_params.get("owner_id")),
                many=True,
            )
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return super().list(request, *args, **kwargs)

from typing import override
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .modules import password
from .models import User
from .serializers import UsersSerializer


class UsersView(APIView):
    @override
    def get(self, request: Request, **kwargs) -> Response:
        is_id_set = 'id' in kwargs

        if is_id_set:
            id = kwargs['id']

            if not self._does_such_user_exist(id):
                return Response(f'user with id={id} doest not exist!', status=status.HTTP_204_NO_CONTENT)

            data = User.objects.get(pk=int(id))
        else:
            data = User.objects.all()

        serializer = UsersSerializer(data, many=not is_id_set)

        return Response(serializer.data, status=status.HTTP_200_OK)


    @override
    def post(self, request: Request) -> Response:
        if not self._set_password(request):
            return Response('Invalid password!', status=status.HTTP_204_NO_CONTENT)

        serializer = UsersSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    # @override
    # def put(self, request: Request) -> Response:
    #     serializer = UsersSerializer(data=request.data)
    #     currentPassword = serializer.data.get('currentPassword')

    #     if not serializer.is_valid():
    #         return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)


    def _set_password(self, request: Request) -> bool:
        user_password = request.data['password']

        if not password.is_password_valid(user_password): return False

        request.data['password'] = password.hash_password(user_password)

        return True


    def _does_such_user_exist(self, pk: int) -> bool:
        return User.objects.filter(pk = pk).exists()

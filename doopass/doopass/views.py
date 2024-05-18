from typing import override
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .modules import password
from .models import User, Storage
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


    @override # Make this working
    def put(self, request: Request) -> Response:
        user = User.objects.get(pk=request.data['id'])

        try:
            self._validate_password(user, request)
        except Exception:
            return Response('Invalid password!', status=status.HTTP_204_NO_CONTENT)

        serializer = UsersSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)
    

    @override
    def delete(self, request: Request) -> Response:
        user = User.objects.get(pk=request.data['id'])

        try:
            self._validate_password(user, request)
        except:
            return Response('Invalid password!', status=status.HTTP_204_NO_CONTENT)

        if 'deleteData' in request.data and request.data['deleteData']:
            self._delete_user_data(user)

        user.delete()

        return Response('Deleted successfully!', status=status.HTTP_200_OK)


    def _validate_password(self, user: User, request: Request) -> None:
        if 'newPassword' in request.data:
            if not self._does_new_password_match(request):
                raise Exception("Invalid password!")
            request.data['password'] = password.hash_password(request.data['newPassword'])
        elif not password.does_password_match(user.password, request.data['password']):
                raise Exception("Invalid password!")
        else:
            request.data['password'] = password.hash_password(request.data['password'])


    def _set_password(self, request: Request) -> bool:
        user_password = request.data['password']

        if not password.is_password_valid(user_password): return False

        request.data['password'] = password.hash_password(user_password)

        return True


    def _does_new_password_match(self, request: Request) -> bool:
        supposed_password = request.data['newPassword']
        current_password = request.data['password']
        user_id = request.data['id']
        user = User.objects.get(pk = user_id)

        if not password.is_password_valid(supposed_password): return False
        if not password.does_password_match(user.password, current_password): return False

        return True
    
    
    def _delete_user_data(self, user: User) -> int:
        storages = Storage.objects.filter(owner = user)

        for storage in storages:
            storage.delete()

        return len(storages)


    def _does_such_user_exist(self, pk: int) -> bool:
        return User.objects.filter(pk = pk).exists()

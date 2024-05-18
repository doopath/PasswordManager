from rest_framework import status
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import User, Storage
from .modules import password
from .serializers import UserSerializer, StorageSerializer


class UserView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        is_id_set = 'id' in kwargs

        if is_id_set:
            id = kwargs['id']

            if not self._does_such_user_exist(id):
                return Response(f'user with id={id} doest not exist!', status=status.HTTP_204_NO_CONTENT)

            data = User.objects.get(pk=int(id))
        else:
            data = User.objects.all()

        serializer = UserSerializer(data, many=not is_id_set)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        if not self._set_password(request):
            return Response('Invalid password!', status=status.HTTP_204_NO_CONTENT)

        serializer = UserSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response("Invalid data passed!", status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request) -> Response:
        user = User.objects.get(pk=request.data['id'])

        try:
            self._validate_password(user, request)
        except Exception:
            return Response('Invalid password!', status=status.HTTP_204_NO_CONTENT)

        serializer = UserSerializer(user, data=request.data)

        if not serializer.is_valid():
            return Response(serializer.data, status=status.HTTP_204_NO_CONTENT)

        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)

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
        user = User.objects.get(pk=user_id)

        if not password.is_password_valid(supposed_password): return False
        if not password.does_password_match(user.password, current_password): return False

        return True

    def _delete_user_data(self, user: User) -> int:
        storages = Storage.objects.filter(owner=user)

        for storage in storages:
            storage.delete()

        return len(storages)

    def _does_such_user_exist(self, pk: int) -> bool:
        return User.objects.filter(pk=pk).exists()


class StorageView(APIView):
    def get(self, request: Request, **kwargs) -> Response:
        if 'id' in kwargs:
            data = Storage.objects.get(pk=kwargs['id'])
            serializer = StorageSerializer(data)
            return Response(serializer.data, status.HTTP_200_OK)
        elif 'owner_id' in kwargs:
            data = Storage.objects.filter(owner_id=kwargs['owner_id'])
            serializer = StorageSerializer(data, len(data) > 1)
            return Response(serializer.data, status.HTTP_200_OK)
        else:
            data = Storage.objects.all()
            serializer = StorageSerializer(data, many=True)
            return Response(serializer.data, status.HTTP_200_OK)

    def post(self, request: Request) -> Response:
        user = User.objects.get(pk=request.data['owner_id'])

        if not self._does_user_password_match(user, request):
            return Response("Invalid password!", status.HTTP_401_UNAUTHORIZED)

        serializer = StorageSerializer(data={
            'name': request.data['name'],
            'owner': request.data['owner_id'],
            'content': request.data['content']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Invalid data passed!", status=status.HTTP_204_NO_CONTENT)

    def put(self, request: Request) -> Response:
        user = User.objects.get(pk=request.data['owner_id'])
        changing_storage = Storage.objects.get(pk=request.data['id'])

        if changing_storage.owner.id != request.data['owner_id']:
            return Response("Owner of the storage cannot be changed!", status.HTTP_304_NOT_MODIFIED)

        if not self._does_user_password_match(user, request):
            return Response("Invalid password!", status.HTTP_401_UNAUTHORIZED)

        serializer = StorageSerializer(changing_storage, data={
            'name': request.data['name'],
            'owner': request.data['owner_id'],
            'content': request.data['content']
        })

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response("Invalid data passed!", status=status.HTTP_204_NO_CONTENT)

    def delete(self, request: Request) -> Response:
        storage = Storage.objects.get(pk=request.data['id'])
        user = storage.owner

        if not self._does_user_password_match(user, request):
            return Response("Invalid password!", status=status.HTTP_401_UNAUTHORIZED)
        
        storage.delete()

        return Response("Successfully deleted!", status=status.HTTP_200_OK)

    def _does_user_password_match(self, user: User, request: Request) -> bool:
        return password.does_password_match(user.password, request.data['password'])


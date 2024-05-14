from typing import override
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.request import Request
from rest_framework import status
from .models import User
from .serializers import UsersSerializer


class UsersView(APIView):
    @override
    def get(self, request: Request, format=None) -> Response:
        id = request.query_params.get('id', '') \
            or request.query_params.get('email', '')
        
        if id:
            data = User.objects.get(pk=int(id))
        else:
            data = User.objects.all()


        serializer = UsersSerializer(data, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)
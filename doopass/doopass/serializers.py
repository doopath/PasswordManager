from typing import override
from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed

from .models import User
from .models import Storage, Backup


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]


class SpecialUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "password", "email"]

    def update(self, instance: User, validated_data: any) -> User:
        instance.set_password(validated_data["password"])
        instance.username = validated_data["username"]
        instance.email = validated_data["email"]
        instance.save()

        return instance


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"

    @override
    def create(self, validated_data: any) -> Storage:
        storage = Storage.objects.create(
            **{
                "name": validated_data["name"],
                "content": validated_data["content"],
                "owner": self.context["request"].user,
            }
        )
        storage.save()

        return storage


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = "__all__"

    @override
    def create(self, validated_data: any) -> Backup:
        storage = Storage.objects.get(pk=self.context["request"].data["storage_id"])
        backup = Backup.objects.create(
            **{
                "name": storage.name,
                "content": storage.content,
                "owner": self.context["request"].user,
                "storage": storage,
            }
        )
        backup.save()

        return backup

    @override
    def update(self, instance: Backup, validated_data: any) -> Backup:
        raise MethodNotAllowed("PUT")

from rest_framework import serializers
from rest_framework.exceptions import MethodNotAllowed
from django.contrib.auth.models import AnonymousUser

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

    def update(self, instance: User, validated_data: dict) -> User:
        instance.username = validated_data["username"] if 'username' in validated_data else instance.username
        instance.email = validated_data["email"] if 'email' in validated_data else instance.email

        if 'password' in validated_data:
            instance.set_password(validated_data["password"])

        instance.save()

        return instance


class StorageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Storage
        fields = "__all__"

    def create(self, validated_data: dict) -> Storage:
        storage = Storage.objects.create(
            **{
                "name": validated_data["name"],
                "content": validated_data["content"],
                "owner": self.context["request"].user,
            }
        )
        storage.save()

        return storage

    def update(self, instance: Storage, validated_data: dict) -> Storage:
        instance.name = validated_data['name'] if 'name' in validated_data else instance.name
        instance.content = validated_data['content'] if 'content' in validated_data else instance.content
        instance.save()

        return instance


class BackupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Backup
        fields = ['id', 'name', 'date', 'owner', 'storage', 'content']

    def create(self, validated_data: dict) -> Backup:
        if type(self.context['request'].user) is AnonymousUser:
            raise serializers.ValidationError("Authentication is required for this method!")

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

    def update(self, instance: Backup, validated_data: dict) -> Backup:
        raise MethodNotAllowed("PUT")

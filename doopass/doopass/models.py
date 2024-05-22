from typing import override
from django.db import models
from django.contrib.auth import models as auth_models
from django.contrib.auth.password_validation import validate_password


class UserManager(auth_models.BaseUserManager):
    @override
    def create_user(self, username: str, email: str, password: str):

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save()

        return user


class User(auth_models.AbstractUser):
    username = models.CharField(max_length=255, unique=True)
    password = models.CharField(validators=[validate_password])
    email = models.EmailField()

    objects = UserManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["password", "email"]


class Storage(models.Model):
    name = models.CharField(max_length=255, default="My Storage")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    content = models.CharField(default="", blank=True)


class Backup(models.Model):
    name = models.CharField(max_length=255, default="My Storage")
    date = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, blank=True)
    content = models.CharField(default="", blank=True)

from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField()
    email = models.EmailField()


class Storage(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
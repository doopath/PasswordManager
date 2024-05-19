from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField()
    email = models.EmailField()


class Storage(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    content = models.CharField(default='', blank=True)


class Backup(models.Model):
    data = models.DateTimeField()
    owner = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    storage = models.ForeignKey(Storage, on_delete=models.DO_NOTHING)
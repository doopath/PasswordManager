from django.db import models


class User(models.Model):
    name = models.CharField(max_length=255)
    password = models.CharField()
    email = models.EmailField()

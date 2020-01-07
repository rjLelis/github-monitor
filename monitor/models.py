from django.db import models

class Profile(models.Model):
    username = models.CharField(max_length=50, unique=True)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    access_token = models.CharField(max_length=40)

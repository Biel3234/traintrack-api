from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    email = models.EmailField(primary_key=True, null=False)
    name = models.CharField(max_length=100, null=False)
    phone = models.CharField(max_length=15, null=False)

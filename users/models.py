from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=False)
    password = models.CharField(max_length=20, null=False)
    phone = models.CharField(max_length=15, null=False)
    category = models.Choices

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
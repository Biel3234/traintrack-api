from django.db import models
from django.contrib.auth.models import AbstractUser
from .managers import UserManager

class User(AbstractUser):

    ROLES_CHOICES = (
        ('admin', 'Admin'),
        ('trainee', 'Trainee'),
        ('trainer', 'Trainer'),
    )
    username = models.CharField(max_length=50)
    email = models.EmailField(unique=True, null=False)
    phone = models.CharField(max_length=15, null=False)
    role = models.CharField(max_length=20, choices=ROLES_CHOICES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    objects = UserManager()

    def __str__(self):
        return self.username
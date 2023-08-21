from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager, AbstractUser, PermissionsMixin
from django.db import models


class CustomUser(AbstractUser):
    username = models.CharField(max_length=30, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username

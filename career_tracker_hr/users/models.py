from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from .constants import CHOICES, HR, STAFF, STUDENT


class CustomUserManager(UserManager):
    pass


class User(AbstractUser):
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=CHOICES,
        default=STUDENT
    )
    
    objects = CustomUserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('role', 'username')

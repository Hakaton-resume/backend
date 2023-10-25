from django.contrib.auth.models import AbstractUser, UserManager
from django.db import models

from .constants import CHOICES, HR, STAFF, STUDENT


class CustomUserManager(UserManager):
    pass


class Company(models.Model):
    name = models.CharField(
        "Название",
        max_length=255,
        null=False,
    )
    logo = models.ImageField(
        "Логотип",
        upload_to="companies/logos/",
        null=True,
        default=None,
    )

    def __str__(self):
        return f"{self.name}"


class StudentUser(models.Model):
    pass


class HRUser(models.Model):
    pass


class StaffUser(models.Model):
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

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils.translation import gettext_lazy as _

from .constants import CHOICES, HR, STAFF, STUDENT


class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, role, **extra_fields):
        email = self.normalize_email(email)

        user = self.model(**extra_fields)
        user.email = email
        user.set_password(password)
        user.save(using=self._db)
        # if 
        return user
    
    def create_superuser(self, email, password, role=STAFF, **extra_fields):
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)

        return self._create_user(email, password, role, **extra_fields)
    
    def create_user(self, email, password, role=STUDENT, **extra_fields):
        if role == STAFF:
            return self.create_superuser(email, password, role, extra_fields)
        return self._create_user(email, password, role, **extra_fields)





class User(AbstractUser):
    username = None
    first_name = models.CharField(_("first name"), max_length=150, blank=True)
    last_name = models.CharField(_("last name"), max_length=150, blank=True)
    email = models.EmailField(_("email address"), unique=True, blank=True)
    role = models.CharField(
        'Роль',
        max_length=9,
        choices=CHOICES,
        default=STUDENT
    )
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        ordering = ('role', 'last_name', 'first_name', )


class Company(models.Model):
    name = models.CharField(
        'Название',
        max_length=255,
        null=False,
    )
    logo = models.ImageField(
        'Логотип',
        upload_to='companies/logos/',
        null=True,
        default=None,
    )

    def __str__(self):
        return f'{self.name}'


class StudentUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,

    )


class HRUser(models.Model):
    company = models.ManyToManyField(Company)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,

    )
    
    class Meta:
        ordering = []


class StaffUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,

    )

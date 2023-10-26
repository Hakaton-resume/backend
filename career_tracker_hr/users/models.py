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


class Skill(models.Model):
    name = models.CharField(
        max_length=50,
        unique=True,
        verbose_name='Навык'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навык'

    def __str__(self):
        return self.name   
    

class StudentUser(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )
    birthdate = models.DateField(
        'Дата рождения',
        null=False,
    )
    brief = models.TextField(
        'О себе',
        max_length=1024,
    )
    photo = models.ImageField(
        'Фотография',
        upload_to='students/photoes/',
        null=True,
    )
    telegram = models.CharField(
        'Telegram',
        max_length=32,
        null=True,
    )
    phone = models.CharField(
        'Телефон',
        max_length=12,
        null=True,
    )
    location = models.CharField(
        'Город',
        max_length=32,
    )
    cv = models.FileField(
        'Резюме',
        upload_to='students/cvs/',
        null=True,
    )
    portfolio = models.FileField(
        'Портфолио',
        upload_to='students/portfolios/',
        null=True,
    )
    education = models.CharField(
        'Основное образование',
        max_length=128,
        null=True,
    )
    education_year = models.IntegerField(
        'Год окончания учебного заведения',
    )
    course = models.CharField(
        'Дополнительное образование',
        max_length=128,
        null=True,
    )
    course_year = models.IntegerField(
        'Год окончания курсов',
    )
    seeking_for = models.BooleanField(
        'Статус поиска',
        default=True,
    )
    position = models.CharField(
        'Должность',
        max_length=128,
        null=False,
    )
    level=models.CharField(
        'Уровень',
        max_length=128,
        null=False,
    )
    experience = models.CharField(
        'Опыт работы',
        max_length=128,
    )
    format = models.CharField(
        'Формат работы',
        max_length=128,
    )
    salary = models.IntegerField(
        'Желаемый доход',
        null=True,
    )
    skills = models.ManyToManyField(
        Skill,
        through='SkillStudent',
        verbose_name='Навыки',
        help_text='Выберите навыки',
        related_name='student_skill',
        blank=False
    )


class SkillStudent(models.Model):
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
        verbose_name='Навык'
    )
    student = models.ForeignKey(
        StudentUser,
        on_delete=models.CASCADE,
        verbose_name='Вакансия'
    )

    class Meta:
        verbose_name = 'Навык студент'
        verbose_name_plural = 'Навык студент'


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

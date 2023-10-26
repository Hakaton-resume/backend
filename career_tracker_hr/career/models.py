from django.db import models
from django.core.validators import RegexValidator
from django.db.models import (CASCADE, CharField, DateTimeField,
                              IntegerField, ImageField, ForeignKey,
                              ManyToManyField, Model, SlugField,
                              TextField, UniqueConstraint)

from users.models import StudentUser, Company


class Tag(Model):
    name = CharField(
        max_length=50,
        unique=True,
        verbose_name='Тег'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Skill(Model):
    name = CharField(
        max_length=50,
        unique=True,
        verbose_name='Навык'
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навык'

    def __str__(self):
        return self.name        


class Activity(models.Model):
    name = models.CharField(
        'Название',
        max_length=128,
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'


class Vacancy(models.Model):
    name = models.CharField(
        'Название',
        max_length=128,
    )
    tags = ManyToManyField(
        Tag,
        through='TagVacancy',
        verbose_name='Теги',
        help_text='Выберите теги',
        related_name='vacancy_tag',
        blank=False
    )
    skills = ManyToManyField(
        Skill,
        through='SkillVacancy',
        verbose_name='Навыки',
        help_text='Выберите навыки',
        related_name='vacancy_skill',
        blank=False
    )
    company = ForeignKey(
        Company,
        on_delete=models.CASCADE
    )
    

    class Meta:
        verbose_name = 'Вакансия'
        verbose_name_plural = 'Вакансии'


class Favourite(Model):
    student = ForeignKey(
        StudentUser,
        on_delete=CASCADE,
        verbose_name='favourite',
        related_name='student'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия',
        related_name='vacancy'
    )

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'


class Resp(Model):
    student = ForeignKey(
        StudentUser,
        on_delete=CASCADE,
        verbose_name='Студент'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия'
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'


class TagVacancy(Model):
    tag = ForeignKey(
        Tag,
        on_delete=CASCADE,
        verbose_name='Тег'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия'
    )

    class Meta:
        verbose_name = 'Тег вакансии'
        verbose_name_plural = 'Теги вакансии'


class SkillVacancy(Model):
    skill = ForeignKey(
        Skill,
        on_delete=CASCADE,
        verbose_name='Навык'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия'
    )

    class Meta:
        verbose_name = 'Навык вакансии'
        verbose_name_plural = 'Навык вакансии'

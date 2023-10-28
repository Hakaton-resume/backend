from django.db import models
from django.core.validators import RegexValidator
from django.db.models import (CASCADE, CharField, DateTimeField,
                              IntegerField, ImageField, ForeignKey,
                              ManyToManyField, Model, SlugField,
                              TextField, UniqueConstraint)

from users.models import StudentUser, Company, Skill
from django.utils.timezone import now


class Tag(Model):
    name = CharField(
        max_length=64,
        unique=True,
        verbose_name='Название'
    )

    class Meta:
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

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
        related_name='favourites'
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
        verbose_name='Вакансия',
        related_name='responses'
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


class Invitation(Model):
    student = ForeignKey(
        StudentUser,
        on_delete=CASCADE,
        verbose_name='Студент'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия',
        related_name='invitation'
    )

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'






class Skill(models.Model):
    name = models.CharField(
        'Навык',
        max_length=128,
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'

        
        
        
        

class Vacancy(models.Model):
    company = models.ForeignKey(
        'users.Company',
        on_delete=models.CASCADE,
    )
    company_name = models.CharField(
        'Название компании',
        max_length=128,
    )
    company_info = models.TextField(
        'Информация о компании',
    )
    location = models.CharField(
        'Город',
        max_length=32,
    )
    pub_date = models.DateField(
        'Дата публикации',
        default=now,
    )
    name = models.CharField(
        'Название',
        max_length=256,
    )
    experience = models.CharField(
        'Опыт работы',
        max_length=32,
    )
    description = models.TextField(
        'Описание',
    )
    responsibilities = models.TextField(
        'Обязанности',
    )
    form = models.CharField(
        'Форма работы',
        max_length=32,
    )
    reject_letter = models.TextField(
        'Отказ соискателю',
    )
    additional_info = models.TextField(
        'Дополнительная информация',
    )
    tags = models.ManyToManyField(
        Tag,
        through='VacancyTags',
        verbose_name='Требуемые навыки',
    )
    )
    skills = models.ManyToManyField(
        Skill,
        through='VacancySkills',
        verbose_name='Требуемые навыки',
    )

    class Meta:
        verbose_name = 'Ваканcия'
        verbose_name_plural = 'Вакансии'


class VacancySkills(models.Model):
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    weigth = models.IntegerField(
        'Вес навыка'
    )


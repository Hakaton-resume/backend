from django.db import models
from django.core.validators import RegexValidator
from django.db.models import (CASCADE, CharField, DateTimeField,
                              IntegerField, ImageField, ForeignKey,
                              ManyToManyField, Model, SlugField,
                              TextField, UniqueConstraint, OneToOneField)

from users.models import StudentUser, Company, Skill
from django.utils.timezone import now


class Tag(Model):
    """Модель тега"""
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


class Vacancy(models.Model):
    """Модель вакансии"""
    company = models.ForeignKey(
        Company,
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
        through='TagVacancy',
        verbose_name='Требуемые навыки',
    )

    skills = models.ManyToManyField(
        Skill,
        through='SkillVacancy',
        verbose_name='Требуемые навыки',
    )
    is_active = models.BooleanField(
        'Активность',
        default=True,
    )

    class Meta:
        verbose_name = 'Ваканcия'
        verbose_name_plural = 'Вакансии'

    def __str__(self):
        return self.name


class Invitation(Model):
    """Модель приглашений"""
    student = ForeignKey(
        StudentUser,
        on_delete=CASCADE,
        verbose_name='Студент'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия',
        related_name='invitations'
    )

    class Meta:
        verbose_name = 'Приглашение'
        verbose_name_plural = 'Приглашения'

    def __str__(self):
        return f'{self.student.user} приглашен на {self.vacancy}'


class Favourite(Model):
    """Модель избранного вакансии"""
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

    def __str__(self):
        return f'{self.student.user} в избранном {self.vacancy}'


class Resp(Model):
    """Модель откликов на вакансии"""
    student = ForeignKey(
        StudentUser,
        on_delete=CASCADE,
        verbose_name='Студент'
    )
    vacancy = ForeignKey(
        Vacancy,
        on_delete=CASCADE,
        verbose_name='Вакансия',
        related_name='response'
    )

    class Meta:
        verbose_name = 'Отклик'
        verbose_name_plural = 'Отклики'
    
    def __str__(self):
        return f'{self.student.user} откликнулся на {self.vacancy}'


class TagVacancy(Model):
    """Модель связи тегов с вакансией"""
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
        constraints = [
            UniqueConstraint(fields=('vacancy', 'tag'), name='vacancy_tag')
        ]

    def __str__(self):
        return f'{self.tag} в {self.vacancy}'


class SkillVacancy(models.Model):
    """Модель связи навыков с вакансией с весовыми коэффициентами"""
    vacancy = models.ForeignKey(
        Vacancy,
        on_delete=models.CASCADE,
    )
    skill = models.ForeignKey(
        Skill,
        on_delete=models.CASCADE,
    )
    weight = models.IntegerField(
        'Вес навыка',
        null=False
    )

    def __str__(self):
        return f'{self.skill} с весом {self.weight} в {self.vacancy}'

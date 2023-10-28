from django.db import models
from django.utils.timezone import now


class Activity(models.Model):
    name = models.CharField(
        'Название',
        max_length=128,
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'


class Skill(models.Model):
    name = models.CharField(
        'Навык',
        max_length=128,
    )

    class Meta:
        verbose_name = 'Навык'
        verbose_name_plural = 'Навыки'


class Tag(models.Model):
    name = models.CharField(
        'Название',
        max_length=64,
    )


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

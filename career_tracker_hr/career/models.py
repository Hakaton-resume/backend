from django.db import models

# Create your models here.
class Activity(models.Model):
    name = models.CharField(
        'Название',
        max_length=128,
    )

    class Meta:
        verbose_name = 'Активность'
        verbose_name_plural = 'Активности'

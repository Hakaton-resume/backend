# Generated by Django 4.2.6 on 2023-10-27 17:31

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Skill',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Навык')),
            ],
            options={
                'verbose_name': 'Навык',
                'verbose_name_plural': 'Навыки',
            },
        ),
        migrations.CreateModel(
            name='Tag',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='Название')),
            ],
        ),
        migrations.CreateModel(
            name='Vacancy',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.CharField(max_length=128, verbose_name='Название компании')),
                ('company_info', models.TextField(verbose_name='Информация о компании')),
                ('location', models.CharField(max_length=32, verbose_name='Город')),
                ('pub_date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата публикации')),
                ('name', models.CharField(max_length=256, verbose_name='Название')),
                ('experience', models.CharField(max_length=32, verbose_name='Опыт работы')),
                ('description', models.TextField(verbose_name='Описание')),
                ('responsibilities', models.TextField(verbose_name='Обязанности')),
                ('form', models.CharField(max_length=32, verbose_name='Форма работы')),
            ],
            options={
                'verbose_name': 'Резюме',
                'verbose_name_plural': 'Резюме',
            },
        ),
    ]

# Generated by Django 4.2.6 on 2023-10-28 10:49

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
        ('career', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='vacancy',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.company'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='skills',
            field=models.ManyToManyField(through='career.SkillVacancy', to='users.skill', verbose_name='Требуемые навыки'),
        ),
        migrations.AddField(
            model_name='vacancy',
            name='tags',
            field=models.ManyToManyField(through='career.TagVacancy', to='career.tag', verbose_name='Требуемые навыки'),
        ),
        migrations.AddField(
            model_name='tagvacancy',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.tag', verbose_name='Тег'),
        ),
        migrations.AddField(
            model_name='tagvacancy',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.vacancy', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='skillvacancy',
            name='skill',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.skill'),
        ),
        migrations.AddField(
            model_name='skillvacancy',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.vacancy'),
        ),
        migrations.AddField(
            model_name='resp',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.studentuser', verbose_name='Студент'),
        ),
        migrations.AddField(
            model_name='resp',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='responses', to='career.vacancy', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.studentuser', verbose_name='Студент'),
        ),
        migrations.AddField(
            model_name='invitation',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='invitation', to='career.vacancy', verbose_name='Вакансия'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='student',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='student', to='users.studentuser', verbose_name='favourite'),
        ),
        migrations.AddField(
            model_name='favourite',
            name='vacancy',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='favourites', to='career.vacancy', verbose_name='Вакансия'),
        ),
    ]
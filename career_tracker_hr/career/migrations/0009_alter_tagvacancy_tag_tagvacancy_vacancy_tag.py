# Generated by Django 4.2.6 on 2023-10-29 20:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('career', '0008_alter_tagvacancy_tag'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tagvacancy',
            name='tag',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='career.tag', verbose_name='Тег'),
        ),
        migrations.AddConstraint(
            model_name='tagvacancy',
            constraint=models.UniqueConstraint(fields=('vacancy', 'tag'), name='vacancy_tag'),
        ),
    ]

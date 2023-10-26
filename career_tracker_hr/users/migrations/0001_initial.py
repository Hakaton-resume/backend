# Generated by Django 4.2.6 on 2023-10-25 21:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import users.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, unique=True, verbose_name='email address')),
                ('role', models.CharField(choices=[('STUDENT', 'Соискатель'), ('HR', 'HR компании-партнера'), ('STAFF', 'Сотрудник Яндекса')], default='student', max_length=9, verbose_name='Роль')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'verbose_name': 'Пользователь',
                'verbose_name_plural': 'Пользователи',
                'ordering': ('role', 'last_name', 'first_name'),
            },
            managers=[
                ('objects', users.models.CustomUserManager()),
            ],
        ),
        migrations.CreateModel(
            name='Company',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название')),
                ('logo', models.ImageField(default=None, null=True, upload_to='companies/logos/', verbose_name='Логотип')),
            ],
        ),
        migrations.CreateModel(
            name='StudentUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('birthdate', models.DateField(verbose_name='Дата рождения')),
                ('brief', models.TextField(max_length=1024, verbose_name='О себе')),
                ('photo', models.ImageField(null=True, upload_to='students/photoes/', verbose_name='Фотография')),
                ('telegram', models.CharField(max_length=32, null=True, verbose_name='Telegram')),
                ('phone', models.CharField(max_length=12, null=True, verbose_name='Телефон')),
                ('location', models.CharField(max_length=32, verbose_name='Город')),
                ('cv', models.FileField(null=True, upload_to='students/cvs/', verbose_name='Резюме')),
                ('portfolio', models.FileField(null=True, upload_to='students/portfolios/', verbose_name='Портфолио')),
                ('education', models.CharField(max_length=128, null=True, verbose_name='Основное образование')),
                ('education_year', models.IntegerField(verbose_name='Год окончания учебного заведения')),
                ('course', models.CharField(max_length=128, null=True, verbose_name='Дополнительное образование')),
                ('course_year', models.IntegerField(verbose_name='Год окончания курсов')),
                ('seeking_for', models.BooleanField(default=True, verbose_name='Статус поиска')),
                ('position', models.CharField(max_length=128, verbose_name='Должность')),
                ('level', models.CharField(max_length=128, verbose_name='Уровень')),
                ('experience', models.CharField(max_length=128, verbose_name='Опыт работы')),
                ('format', models.CharField(max_length=128, verbose_name='Формат работы')),
                ('salary', models.IntegerField(null=True, verbose_name='Желаемый доход')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='StaffUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HRUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company', models.ManyToManyField(to='users.company')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': [],
            },
        ),
    ]

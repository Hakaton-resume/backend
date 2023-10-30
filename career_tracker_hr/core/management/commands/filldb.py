import os
from datetime import date, timedelta
from pathlib import Path
from random import choice, randint, randrange, shuffle

from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management import base

from .fixtures import NAMES, SURNAMES, LNAMES, LOCATIONS, CAREERS, BRIEFS, SKILLS, JOBS, UNIVERCITIES, COURSES, ACTIVITIES

from users.models import Activity, Skill, StudentUser, StudentsActivities, SkillStudent


User = get_user_model()

def transliterate(v):
    table = str.maketrans({
        'а':'a','б':'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 
        'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'ju', 'я': 'ya'
    })
    return v.lower().translate(table)

def getlogin(n1, n2, n3):
    table = str.maketrans({
        'а':'a','б':'b', 'в': 'v', 'г': 'g', 'д': 'd', 'е': 'e', 'ё': 'e', 'ж': 'zh', 'з': 'z', 
        'и': 'i', 'й': 'i', 'к': 'k', 'л': 'l', 'м': 'm', 'н': 'n', 'о': 'o', 'п': 'p', 'р': 'r',
        'с': 's', 'т': 't', 'у': 'u', 'ф': 'f', 'х': 'h', 'ц': 'c', 'ч': 'ch', 'ш': 'sh', 'щ': 'sch',
        'ъ': '', 'ы': 'y', 'ь': '', 'э': 'e', 'ю': 'ju', 'я': 'ya'
    })
    login = (n1 + n2[0] + n3[0])
    login = login.lower()
    login = login.translate(table)
    login = f'{login}{randint(1, 999):03}@{choice(["gmail.com", "yandex.ru", "mail.ru", "yahoo.com", "rambler.ru", "outlook.com"])}'
    return login
    # return f'{transliterate(n1 + n2[1] + n3[1])}@{choice(["gmail.com", "yandex.ru", "mail.ru", "yahoo.com", "rambler.ru", "outlook.com"])}'


class Command(base.BaseCommand):
    def handle(self, *args, **options):
        photoes = {
            'f': os.listdir(path=os.path.join(settings.BASE_DIR, 'core/management/commands/photoes/f/')),
            'm': os.listdir(path=os.path.join(settings.BASE_DIR, 'core/management/commands/photoes/m/')),
        }

        Activity.objects.all().delete()
        Skill.objects.all().delete()

        for a in ACTIVITIES:
            activity = Activity(
                name=a
            )
            activity.save()

        for _ in range(50):
            a = choice(['m', 'f'])
            lastname, firstname, surname = choice(LNAMES[a]), choice(NAMES[a]), choice(SURNAMES[a])
            login = getlogin(lastname, firstname, surname)
            photo = choice(photoes[a])
            photo = Path(os.path.join(settings.BASE_DIR, f'core/management/commands/photoes/{a}/{photo}'))
            # year = randint(1973, 2005)
            dob = date(1973, 1, 1) + timedelta(days=randrange((date(2005, 12, 31) - date(1973, 1, 1)).days))
            location = choice(LOCATIONS)
            carrer = choice(CAREERS)
            job = choice(JOBS[carrer])
            brief = choice(BRIEFS[carrer])
            skills = []
            for _ in range(choice([1, 2])):
                skills.append(choice(SKILLS['critical'][carrer]))
            for _ in range(choice([0, 1, 2])):
                skills.append(choice(SKILLS['important'][carrer]))
            for _ in range(choice([0, 1, 2])):
                skills.append(choice(SKILLS['optional'][carrer]))
            phone = f'+7{randint(900, 999)}{randint(1,9999999):07}'
            telegram = f'@{login.split("@")[0]}'
            letter = Path(os.path.join(settings.BASE_DIR, 'core/management/commands/data/letter.pdf'))
            resume = Path(os.path.join(settings.BASE_DIR, 'core/management/commands/data/resume.pdf'))
            univercity = choice(UNIVERCITIES)
            univercity_year = dob.year + randint(20, 27)
            course = choice(COURSES)
            course_year = 2023 - randint(0, 3)
            level = choice(['junior', 'middle'])
            format = choice(['удаленно', 'гибрид', 'офис'])
            experience = choice([0, 6, 12, 24, 36])
            salary = choice([12_000, 25_000, 50_000, 100_000])

            print('*'*10)
            print(f'{login}: {lastname}, {firstname} {surname} - {dob} - {location} - [{photo}]')
            print(f'{phone} - {telegram}')
            print(f'{univercity} - {univercity_year}')
            print(f'{course} - {course_year}')
            print(f'{job} : {level}\n{brief}')
            print(f'{skills}')
            print(f'{resume} : {letter}')
            print(f'Уровень зарплатных ожиданий: {salary}')
            print(f'{format}')
            print(f'{experience}')
            print('*'*10)

            

            user = User(
                first_name=f'{firstname} {surname}',
                last_name=lastname,
                email=login,
                password=login,
            )
            user.save()
            student = StudentUser(
                user=user,
                birthdate=dob,
                brief=brief,
                telegram=telegram,
                phone=phone,
                location=location,
                education=univercity,
                education_year=univercity_year,
                course=course,
                course_year=course_year,
                seeking_for=True,
                position=job,
                level=level,
                experience=experience,
                format=format,
                salary=salary,
            )
            with photo.open(mode='rb') as f:
                student.photo = File(f, name=photo.name)
                student.save()
            with resume.open(mode='rb') as f:
                student.cv = File(f, name=resume.name)
                student.save()
            with letter.open(mode='rb') as f:
                student.portfolio = File(f, name=letter.name)
                student.save()

            activities = ACTIVITIES.copy()
            shuffle(activities)
            activities_count = randint(0, len(activities))

            for n in range(activities_count):
                activity = Activity.objects.get(name=activities[n])
                student_activity = StudentsActivities(
                    student=student,
                    activity=activity
                )
                student_activity.save()

            for s in skills:
                skill, created = Skill.objects.get_or_create(name=s)
                if created:
                    skill.save()
                skill_students = SkillStudent(
                    skills=skill,
                    student=student
                )
                skill_students.save()
        pass

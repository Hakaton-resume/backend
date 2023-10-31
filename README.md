# Хакатон Карьерный трекер
![example workflow](https://github.com/Hakaton-resume/backend/actions/workflows/workflow.yml/badge.svg)

## Задача
Разработать внутренний сервис найма в карьерном трекере, который предоставляет возможность компаниям-партнерам Яндекс Практикума работать с базой заинтересованных кандидатов и отбирать не только текущих студентов, но и выпускников уровня middle и выше.


## Возможности:
- Просматривать списки кандидатов ранжированные по проценту совпадений с вакансией 
- Просматривать отклики кандидатов на опубликованные вакансии 
- Добавлять заинтересовавших кандидатов в избранное
- Отправлять приглашения на собеседования понравившимся кандидатам

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

#### PM:
- [Боброва Анастасия](https://github.com/bobrova93)

#### Команда дизайнеров
- Дзюба Владислав
- Ламтюгина Александра
- [Синицкая Анна](https://github.com/Sinitskayaya)

#### Команда fromtend-разработчиков
- [Карпов Кирилл](https://github.com/RinVeber)
- [Лысцов Антон](https://github.com/777toha)
- Рагойжа Дмитрий


#### Команда backend-разработчиков:
- [Бескровный Борис](https://github.com/beskrovniibv)
- [Пашкова Юлия](https://github.com/Jullitka)

## Запуск проекта

#### Клонируйте репозиторий
```
https://github.com/Hakaton-resume/backend/tree/main
```
#### Создайте файл содержащий переменные виртуального окружения .env на примере .env.example
```
SECRET_KEY = <Секретный ключ>
DB_ENGINE=<django.db.backends.postgresql>
DB_NAME=<имя базы данных postgres>
DB_USER=<пользователь бд>
DB_PASSWORD=<пароль>
DB_HOST=<db>
DB_PORT=<5432>
```
#### Разверните контейнеры из папки infra и выполните миграции
```
sudo docker compose up -d --build
sudo docker compose exec career_tracker_hr bash -c 'python manage.py migrate'
```
#### Создайте суперюзера
```
sudo docker compose exec career_tracker_hr bash -c 'python manage.py createsuperuser'
```
####  Cоберите статику
```
sudo docker compose exec career_tracker_hr bash -c 'python manage.py collectstatic --no-input'
```
####  Загрузите данные
```
sudo docker compose exec career_tracker_hr bash -c 'python manage.py filldb'
```
#### Проект доступен по адресу https://career-tracker.duckdns.org  

## Документация

Swagger https://career-tracker.duckdns.org/swagger/  
Redoc https://career-tracker.duckdns.org/redoc/  


19 - 31 октября 2023 года

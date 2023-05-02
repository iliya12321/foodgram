# Foodrgam - продуктовый помощник

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)

## Описание проекта
Онлайн-сервис Foodgram («Продуктовый помощник») создан для начинающих кулинаров и опытных гурманов. В сервисе пользователи смогут публиковать рецепты, подписываться на публикации других пользователей, добавлять понравившиеся рецепты в список «Избранное», а перед походом в магазин скачивать в формате .txt сводный список продуктов, необходимых для приготовления одного или нескольких выбранных блюд.

Проект разворачивается в Docker контейнерах: backend-приложение API, PostgreSQL-база данных, nginx-сервер и frontend-контейнер.

Реализовано CI и CD проекта. При пуше изменений в главную ветку проект автоматические тестируется на соотвествие требованиям PEP8. После успешного прохождения тестов, на git-платформе собирается образ backend-контейнера Docker и автоматически размещается в облачном хранилище DockerHub. Размещенный образ автоматически разворачивается на боевом сервере вмете с контейнером веб-сервера nginx и базой данных PostgreSQL.


## Стек технологий:
- Python 3.7
- Django 2.2
- Djangorestframework 3.12
- PostgreSQL 
- Docker

---

### Развертывание на сервере:

1. Установите на сервере `docker` и `docker-compose`.
2. Выполните команду `docker-compose up -d --buld`.
3. Выполните миграции `docker-compose exec backend python manage.py migrate`.
4. Создайте суперюзера `docker-compose exec backend python manage.py createsuperuser`.
5. Соберите статику `docker-compose exec backend python manage.py collectstatic --no-input`.
6. Заполните базу ингредиентами `docker-compose exec backend python manage.py load_ingredients`.
7. **Для корректного создания рецепта через фронт, надо создать пару тегов в базе через админку.**

## Автор

Воробьев Илья

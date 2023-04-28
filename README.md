# Foodrgam
Foodgram это продуктовый помощник, вы можете зарегестрироваться на сайте, и создавать рецепты, либо добавить понравившайся вам рецепт к себе в избранно, так же можно скачать список ингредиентов для рецепта, и пойти с ним в магазин :)

Реализована подписка на авторов, смена пароля, добавление рецепта в избранное, скачивание списка ингредиентов для рецепта.

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
8. Документация к API находится по адресу: <http://158.160.33.43/api/docs/redoc.html>.

## Автор

Воробьев Илья
from django.core.exceptions import ValidationError

from core.enums import Limits
from recipes.models import Ingredient, Tag


def validate_ingredients(data):
    """Валидация ингредиентов и количества."""
    if not data:
        raise ValidationError({'ingredients': ['Не переданы ингредиенты.']})

    unique_ingredient = []
    for ingredient in data:
        if not ingredient.get('id'):
            raise ValidationError({'ingredients': ['Отсутствует id ингредиента.']})

        id = ingredient.get('id')
        if not Ingredient.objects.filter(id=id).exists():
            raise ValidationError('Ингредиента нет в БД.')

        if id in unique_ingredient:
            raise ValidationError(
                'Нельзя дублировать имена ингредиентов.'
            )
        unique_ingredient.append(id)

        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError(
                f"""Количество не может быть менее
                {Limits.MIN_COOKING_TIME_AND_AMOUNT}"""
            )
    return data


def validate_tags(data):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not data:
        raise ValidationError('Хотя бы один тэг должен быть указан.')

    for tag in data:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError('Тэг отсутствует в БД.')
    return data


def validate_time(value):
    """Валидация поля модели - время приготовления."""
    if value < 1:
        raise ValidationError(
            f"""Время приготовления не может быть менее
            {Limits.MIN_COOKING_TIME_AND_AMOUNT}"""
        )

from django.core.exceptions import ValidationError

from core.enums import Limits
from recipes.models import Ingredient, Tag


def validate_ingredients(ingredients):
    """Валидация ингредиентов и количества."""
    if not ingredients:
        raise ValidationError('Не переданы ингредиенты.')

    unique_ingredient = []
    for ingredient in ingredients:
        if not ingredient.get('id'):
            raise ValidationError('Отсутствует id ингредиента.')

        ingredient_id = ingredient.get('id')
        if not Ingredient.objects.filter(id=ingredient_id).exists():
            raise ValidationError('Ингредиента нет в БД.')

        if ingredient_id in unique_ingredient:
            raise ValidationError(
                'Нельзя дублировать имена ингредиентов.'
            )
        unique_ingredient.append(ingredient_id)

        amount = int(ingredient.get('amount'))
        if amount < 1:
            raise ValidationError(
                f"""Количество не может быть менее
                {Limits.MIN_COOKING_TIME_AND_AMOUNT}"""
            )
    return ingredients


def validate_tags(tags):
    """Валидация тэгов: отсутствие в request, отсутствие в БД."""
    if not tags:
        raise ValidationError('Хотя бы один тэг должен быть указан.')

    tags_list = []
    for tag in tags:
        if not Tag.objects.filter(id=tag).exists():
            raise ValidationError('Тэг отсутствует в БД.')
        if tag in tags_list:
            raise ValidationError(
                'Тэги должны быть уникальными!'
            )
        tags_list.append(tag)
    return tags


def validate_time(cooking_time):
    """Валидация поля модели - время приготовления."""
    if int(cooking_time) < 1:
        raise ValidationError(
            f"""Время приготовления не может быть менее
            {Limits.MIN_COOKING_TIME_AND_AMOUNT}"""
        )
    return cooking_time

"""Настройки параметров."""
from enum import IntEnum


class Limits(IntEnum):
    # Максимальная длина email (User)
    MAX_LEN_EMAIL_FIELD = 254
    # Максимальная длина строковых полей моделей в приложении "users"
    MAX_LEN_USERS_CHARFIELD = 150
    # Максимальная длина password (User)
    MAX_LEN_PASSWORD = 150
    # Максимальная длина color (Tag)
    MAX_LEN_COLOR = 7
    # Максимальная длина строковых полей моделей в приложении "recipes"
    MAX_LEN_RECIPES_CHARFIELD = 64
    # Максимальная длина единицы измеренияs моделей в приложении "recipes"
    MAX_LEN_MEASUREMENT = 256
    # Максимальная длина название рецепта
    MAX_LEN_NAME = 200
    # Минимальное время приготовления рецепта в минутах
    # и количество ингридиента в рецепте
    MIN_COOKING_TIME_AND_AMOUNT = 1
    # Минимальное количество ингридиентов для рецепта

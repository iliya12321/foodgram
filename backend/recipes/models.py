from django.core.validators import MinValueValidator
from django.db.models import (
    CASCADE,
    CharField,
    DateTimeField,
    ForeignKey,
    ImageField,
    ManyToManyField,
    Model,
    PositiveSmallIntegerField,
    SlugField,
    TextField,
    UniqueConstraint,
)

from core.enums import Limits
from recipes.validators import hex_color_validator
from users.models import User


class Tag(Model):
    """Тег."""
    name = CharField(
        verbose_name='Название тега',
        max_length=Limits.MAX_LEN_RECIPES_CHARFIELD.value,
        unique=True,
    )
    color = CharField(
        verbose_name='Цвет тега',
        max_length=Limits.MAX_LEN_COLOR.value,
        unique=True,
        validators=[hex_color_validator],
    )
    slug = SlugField(
        max_length=Limits.MAX_LEN_RECIPES_CHARFIELD.value,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(Model):
    """Ингиридиент."""
    name = CharField(
        verbose_name='Название ингридиента',
        max_length=Limits.MAX_LEN_RECIPES_CHARFIELD.value,
    )
    measurement_unit = CharField(
        verbose_name='Единицы измерения ингридиента',
        max_length=Limits.MAX_LEN_MEASUREMENT.value,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name='unique_ingredient',
            ),
        ]

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'


class Recipe(Model):
    """Рецепт блюда."""
    author = ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=CASCADE,
    )
    ingredients = ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Список ингридиентов',
        through='IngredientAmount',
    )
    tags = ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список id тегов',
    )
    image = ImageField(
        verbose_name='Картинка блюда',
        upload_to='recipe_images/',
    )
    name = CharField(
        verbose_name='Название',
        max_length=Limits.MAX_LEN_NAME.value,
    )
    text = TextField(
        verbose_name='Описание',
        help_text='Введите рецепт',
    )
    cooking_time = PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                Limits.MIN_COOKING_TIME_AND_AMOUNT.value,
                message=(
                    f"""Убедитесь, что введенное число больше или равно
                    {Limits.MIN_COOKING_TIME_AND_AMOUNT.value}"""
                ),
            ),
        ],
    )
    pub_date = DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('-pub_date',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return f'{self.name}. Автор: {self.author.username}'


class IngredientAmount(Model):
    """Количество ингридиентов в рецепте."""
    recipe = ForeignKey(
        Recipe,
        related_name='ingredient',
        verbose_name='Рецепт',
        on_delete=CASCADE,
    )
    ingredient = ForeignKey(
        Ingredient,
        related_name='recipe',
        verbose_name='Ингридиент',
        on_delete=CASCADE,
    )
    amount = PositiveSmallIntegerField(
        verbose_name='Количество ингридиентов',
        validators=[
            MinValueValidator(
                Limits.MIN_COOKING_TIME_AND_AMOUNT.value,
                message=(
                    f"""Убедитесь, что введенное число больше или равно
                    {Limits.MIN_COOKING_TIME_AND_AMOUNT.value}"""
                ),
            ),
        ],
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredient alredy added',
            ),
        ]

    def __str__(self):
        return f'{self.amount} {self.ingredient}'


class Favorite(Model):
    """Избранные рецепты."""
    recipe = ForeignKey(
        Recipe,
        related_name='in_favorites',
        verbose_name='Понравившиеся рецепты',
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        related_name='favorites',
        verbose_name='Автор списка избранного',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favourite_recipe',
            ),
        ]

    def __str__(self):
        return f'Рецепт: {self.recipe} в избранном у {self.user.username}'


class ShoppingCart(Model):
    """Список покупок."""
    recipe = ForeignKey(
        Recipe,
        related_name='in_carts',
        verbose_name='Рецепты в списке покупок',
        on_delete=CASCADE,
    )
    user = ForeignKey(
        User,
        related_name='carts',
        verbose_name='Владелец списка покупок',
        on_delete=CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_recipe_in_shopping_cart',
            ),
        ]

    def __str__(self):
        return f'Рецепт {self.recipe} в списке покупок у {self.user.username}'

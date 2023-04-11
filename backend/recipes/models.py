from django.db import models
from django.core.validators import MinValueValidator

from users.models import User


class Tag(models.Model):
    """Тег """
    name = models.CharField(
        verbose_name='Название тега',
        max_length=255,
        unique=True,
    )
    color = models.CharField(
        verbose_name='Цвет тега',
        max_length=10,
        unique=True,
    )
    slug = models.SlugField(
        max_length=50,
        unique=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Тег'
        verbose_name_plural = 'Теги'

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    """Ингиридиент"""
    name = models.CharField(
        verbose_name='Название ингридиента',
        max_length=150,
    )
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения ингридиента',
        max_length=24,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Ингридиент'
        verbose_name_plural = 'Ингридиенты'
        constraints = [
            models.UniqueConstraint(
                fields=['name', 'measurement_unit'],
                name = 'unique_ingredient',
            ),
        ]

    def __str__(self):
        return self.name


class Recipe(models.Model):
    """Рецепт блюда"""
    author = models.ForeignKey(
        User,
        related_name='recipes',
        verbose_name='Автор рецепта',
        on_delete=models.CASCADE,
    )
    ingredients = models.ManyToManyField(
        Ingredient,
        related_name='recipes',
        verbose_name='Список ингридиентов',
        through='IngredientAmount',
    )
    tags = models.ManyToManyField(
        Tag,
        related_name='recipes',
        verbose_name='Список id тегов',
    )
    image = models.ImageField(
        verbose_name='Картинка, закодированная в Base64',
        upload_to='recipe_images/',
    )
    name = models.CharField(
        verbose_name='Название',
        max_length=200,
    )
    text = models.TextField(
        verbose_name='Описание',
        help_text='Введите рецепт',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления в минутах',
        validators=[
            MinValueValidator(
                1,
                message='Убедитесь, что введенное число больше или равно 1',
            ),
        ],
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        db_index=True,
    )

    class Meta:
        ordering = ('name',)
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self):
        return self.name


class IngredientAmount(models.Model):
    """Количество ингридиентов в рецепте"""
    recipe = models.ForeignKey(
        Recipe,
        related_name='ingredient',
        verbose_name='Рецепт',
        on_delete=models.CASCADE,
    )
    ingredient = models.ForeignKey(
        Ingredient,
        related_name='recipe',
        verbose_name='Ингридиент',
        on_delete=models.CASCADE,
    )
    amount = models.PositiveSmallIntegerField(
        verbose_name='Количество ингридиентов',
        validators=[
            MinValueValidator(
                1,
                message='Убедитесь, что введенное число больше или равно 1',
            ),
        ],
    )

    class Meta:
        verbose_name = 'Количество ингридиента'
        verbose_name_plural = 'Количество ингридиентов'
        constraints = [
            models.UniqueConstraint(
                fields=['ingredient', 'recipe'],
                name='ingredient alredy added',
            ),
        ]

    def __str__(self):
        return '{} {}'.format(self.amount, self.ingredient)

    
class Favorite(models.Model):
    """Избранные рецепты"""
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_favorites',
        verbose_name='Понравившиеся рецепты',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='favorites',
        verbose_name='Автор списка избранного',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Избранный рецепт'
        verbose_name_plural = 'Избранные рецепты'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name = 'unique_favourite_recipe',
            ),
        ]

    def __str__(self):
        return 'Рецепт {} в избранном у {}'.format(self.recipe, self.user)


class ShoppingCart(models.Model):
    """Список покупок"""
    recipe = models.ForeignKey(
        Recipe,
        related_name='in_carts',
        verbose_name='Рецепты в списке покупок',
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        related_name='carts',
        verbose_name='Владелец списка покупок',
        on_delete=models.CASCADE,
    )

    class Meta:
        verbose_name = 'Рецепт в списке покупок'
        verbose_name_plural = 'Рецепты в списке покупок'
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name = 'unique_recipe_in_shopping_cart',
            ),
        ]

    def __str__(self):
        return 'Рецепт {} в списке покупок у {}'.format(self.recipe, self.user)

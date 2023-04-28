from django.contrib.admin import (
    ModelAdmin,
    register,
    site,
    TabularInline,
)
from django.utils.safestring import mark_safe

from recipes.models import (
    Recipe, Ingredient, ShoppingCart, Favorite, Tag, IngredientAmount,
)

site.site_header = 'Администрирование Foodgram-project-react'
EMPTY_VALUE_DISPLAY = '--пусто--'


class IngredientInline(TabularInline):
    model = IngredientAmount


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'name', 'author', 'get_image', 'count_favorites',
    )
    list_filter = (
        'name', 'author__username', 'tags__name'
    )
    search_fields = ('author__username', 'name', 'tags__name')
    fields = (
        ('name', 'cooking_time',),
        ('author', 'tags',),
        ('text',),
        ('image',),
    )
    inlines = (IngredientInline, )
    empty_value_display = EMPTY_VALUE_DISPLAY

    def count_favorites(self, obj):
        return obj.in_favorites.count()

    count_favorites.short_description = 'В избранном'

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="80" hieght="30"')

    get_image.short_description = 'Изображение'


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('id', 'name', 'measurement_unit')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(IngredientAmount)
class IngredientAmountAdmin(ModelAdmin):
    list_display = ('id', 'recipe', 'ingredient', 'amount')
    list_filter = ('recipe', 'ingredient')
    search_fields = ('recipe__name', 'ingredient__name')
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Favorite)
class FavoutriteAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    list_filter = ('user', 'recipe')
    search_fields = ('user__username', 'recipe__name')
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('id', 'name','color', 'slug')
    list_filter = ('name',)
    search_fields = ('name',)
    empty_value_display = EMPTY_VALUE_DISPLAY


@register(ShoppingCart)
class ShoppingCartAdmin(ModelAdmin):
    list_display = ('id', 'user', 'recipe')
    empty_value_display = EMPTY_VALUE_DISPLAY

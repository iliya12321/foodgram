from django.contrib import admin

from recipes.models import (
    Recipe, Ingredient, ShoppingCart, Favoutrite, Tag, IngredientAmount,
)


EMPTY_VALUE_DISPLAY = '--пусто--'


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'author',
    )
    list_filter = (
        'author',
        'name',
        'tags',
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY

    @staticmethod
    def amount_favourites(self, obj):
        return obj.in_favorites.count()


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'measurement_unit',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'ingredient',
        'amount',
    )
    list_filter = (
        'recipe',
        'ingredient',
        'amount',
    )
    search_fields = (
        'recipe',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Favoutrite)
class FavoutriteAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'recipe',
    )
    list_filter = (
        'user',
    )
    search_fields = (
        'recipe',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'color',
    )
    list_filter = (
        'name',
    )
    search_fields = (
        'name',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY


@admin.register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = (
        'recipe',
        'user',
    )
    list_filter = (
        'recipe',
        'user',
    )
    search_fields = (
        'recipe',
    )
    empty_value_display = EMPTY_VALUE_DISPLAY

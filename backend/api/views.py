from django.shortcuts import render
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, SAFE_METHODS

from api.permissions import IsAuthorAdminOrReadOnly
from api.serializers import (
    TagsSerialiser,
    IngredientSerialiser,
    RecipeGetSerialiser,
    RecipeChangeSerialiser,
)
from recipes.models import (
    Tag,
    Ingredient,
    Recipe,
    Favoutrite,
    ShoppingCart,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работает с тэгами.
    Изменение и создание тэгов разрешено только админам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagsSerialiser
    permission_classes = (AllowAny, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работает с ингридиентами.
    Изменение и создание тэгов разрешено только админам.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerialiser
    permission_classes = (AllowAny, )


class PecipeViewSet(viewsets.ModelViewSet):
    """
    Работает с рецептами.
    Для добавление рецепта необходимо быть авторизованным.
    Удаление и редактирование рецепта разрешено только его автором или администратором.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorAdminOrReadOnly, )

    def get_serializer_class(self):
        if self.action in SAFE_METHODS:
            return RecipeGetSerialiser
        return RecipeChangeSerialiser
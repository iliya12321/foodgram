from datetime import datetime as dt
from django.db.models import F, Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from rest_framework.status import (
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST
)
from rest_framework.response import Response

from api.serializers import FavoriteSerializer
from backend.settings import DATE_TIME_FORMAT
from recipes.models import Recipe, Ingredient


def post_method(model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        return Response(
            'Уже существует', status=HTTP_400_BAD_REQUEST
        )
    recipe = get_object_or_404(Recipe, pk=pk)
    instance = model.objects.create(user=user, recipe=recipe)
    serializer = FavoriteSerializer(instance)
    return Response(data=serializer.data, status=HTTP_201_CREATED)


def delete_method(model, user, pk):
    if model.objects.filter(user=user, recipe__id=pk).exists():
        model.objects.filter(
            user=user, recipe__id=pk
        ).delete()
        return Response(status=HTTP_204_NO_CONTENT)
    return Response(status=HTTP_400_BAD_REQUEST)


def download_cart(user):
    filename = f'{user.username}_shopping_list.txt'
    shopping_list = [
        f'Список покупок для:\n\n{user.first_name}\n'
        f'{dt.now().strftime(DATE_TIME_FORMAT)}\n'
    ]

    ingredients = Ingredient.objects.filter(
        recipe__recipe__in_carts__user=user
    ).values(
        'name',
        measurement=F('measurement_unit')
    ).annotate(amount=Sum('recipe__amount'))

    for ing in ingredients:
        shopping_list.append(
            f'{ing["name"]}: {ing["amount"]} {ing["measurement"]}'
        )
    shopping_list.append('\nПосчитано в Foodgram')
    shopping_list = '\n'.join(shopping_list)
    response = HttpResponse(
        shopping_list, content_type='text.txt; charset=utf-8'
    )
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response

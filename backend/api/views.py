from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, SAFE_METHODS, IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
)

from api.filters import IngredientSearchFilter, RecipeFilter
from api.pagination import CustomPagination
from api.permissions import IsAuthorAdminOrReadOnly
from api.serializers import (
    TagsSerializer,
    IngredientSerializer,
    RecipeChangeSerializer,
    RecipeGetSerializer,
)
from api.utlis import post_method, delete_method, download_cart
from recipes.models import (
    Favorite,
    Ingredient,
    Recipe,
    ShoppingCart,
    Tag,
)


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работает с тэгами.
    Изменение и создание тэгов разрешено только админам.
    """
    queryset = Tag.objects.all()
    serializer_class = TagsSerializer
    pagination_class = None
    permission_classes = (AllowAny, )


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Работает с ингридиентами.
    Изменение и создание ингредиентов разрешено только админам.
    """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    permission_classes = (AllowAny, )
    filter_backends = [IngredientSearchFilter]
    search_fields = ('^name',)


class RecipeViewSet(viewsets.ModelViewSet):
    """
    Работает с рецептами.
    Для добавление рецепта необходимо быть авторизованным.
    Удаление и редактирование рецепта
    разрешено только его автором или администратором.
    """
    queryset = Recipe.objects.all()
    permission_classes = (IsAuthorAdminOrReadOnly, )
    pagination_class = CustomPagination
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeGetSerializer
        return RecipeChangeSerializer

    @action(
        detail=True,
        methods=('post', 'delete'),
        permission_classes=(IsAuthenticated, ),
    )
    def favorite(self, request, pk):
        """
        Работает с избранными рецептами.
        Удалять и добавлять в избранное
        может только авторизованный пользователь.
        """
        if self.request.method == 'POST':
            return post_method(Favorite, request.user, pk)
        return delete_method(Favorite, request.user, pk)

    @action(
        detail=True,
        methods=['post', 'delete'],
        permission_classes=(IsAuthenticated, )
    )
    def shopping_cart(self, request, pk):
        """
        Работает со списком покупок.
        Удалять и добавлять в список покупок
        может только авторизованный пользователь.
        """
        if request.method == 'POST':
            return post_method(ShoppingCart, request.user, pk)
        return delete_method(ShoppingCart, request.user, pk)

    @action(
        detail=False,
        methods=['get'],
        permission_classes=(IsAuthenticated, )
    )
    def download_shopping_cart(self, request):
        """
        Позволяет скачать файл списка покупок.
        Доступно только авторизованным пользователям.
        """
        user = request.user
        if not user.carts.exists():
            return Response(status=HTTP_400_BAD_REQUEST)
        return download_cart(user)

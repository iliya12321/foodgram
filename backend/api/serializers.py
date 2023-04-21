from api.fields import Base64ImageField
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    Serializer,
    SerializerMethodField,
)

from core.validators import (
    validate_ingredients,
    validate_tags,
    validate_time,
)
from recipes.models import (
    Favorite,
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag,
    ShoppingCart,
)
from users.serializers import CustomUserSerializer, ShortRecipeSerializer


class TagsSerializer(ModelSerializer):
    """Сериализатор для вывода тегов."""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientSerializer(ModelSerializer):
    """Сериализатор для вывода ингридиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = ('__all__', )


class IngredientAmountSerializer(ModelSerializer):
    """Сериализатор для вывода количества ингредиентов."""
    id = ReadOnlyField(source='ingredient.id')
    name = ReadOnlyField(source='ingredient.name')
    measurement_unit = ReadOnlyField(
        source='ingredient.measurement_unit'
    )

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(Serializer):
    """Сериализатор для добавления ингредиентов."""
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField()


class RecipeGetSerializer(ModelSerializer):
    """Сериализатор для отображения рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingredients = SerializerMethodField(read_only=True)
    tags = TagsSerializer(many=True, read_only=True)
    image = Base64ImageField()
    is_favorited = SerializerMethodField()
    is_in_shopping_cart = SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time',
        )
        read_only_fields = ('is_favorited', 'is_in_shopping_cart')

    def get_ingredients(self, obj):
        """Получаем все ингридиенты рецепта."""
        queryset = IngredientAmount.objects.filter(recipe=obj).all()
        return IngredientAmountSerializer(queryset, many=True).data

    def get_presence(self, model, obj):
        user = self.context.get('request').user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        """Статус - рецепт в избранном или нет."""
        return self.get_presence(Favorite, obj)

    def get_is_in_shopping_cart(self, obj):
        """Статус - рецепт в списке покупок или нет."""
        return self.get_presence(ShoppingCart, obj)


class RecipeChangeSerializer(ModelSerializer):
    """Сериализатор для добавления рецепта."""
    tags = PrimaryKeyRelatedField(
        queryset=Tag.objects.all(), many=True,
    )
    ingredients = AddIngredientSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'tags',
            'image',
            'name',
            'text',
            'cooking_time',
        )

    def add_ingredients(self, ingredients_list, recipe):
        """Создание уникальных записей: ингредиент - рецепт - количество."""
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            ) for ingredient in ingredients_list
        ])

    def validate(self, data):
        validate_tags(self.initial_data.get('tags')),
        validate_ingredients(
            self.initial_data.get('ingredients')
        )
        validate_time(
            self.initial_data.get('cooking_time')
        )
        return data

    def create_tags(self, data, recipe):
        """Отправка на валидацию и создание тэгов у рецепта."""
        for tag in data:
            recipe.tags.add(tag)

    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.create_tags(tags, recipe)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerializer(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.create_tags(validated_data.pop('tags'), instance)
        self.add_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)


class FavoriteSerializer(ModelSerializer):
    """
    Сериализатор для списка избранного
    """
    class Meta:
        model = Favorite
        fields = ('user', 'recipe')

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return ShortRecipeSerializer(
            instance.recipe, context=context
        ).data

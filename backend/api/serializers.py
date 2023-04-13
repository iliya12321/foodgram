from api.fields import Base64ImageField
from rest_framework.serializers import (
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    ReadOnlyField,
    Serializer,
    SerializerMethodField,
    ValidationError,
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
        fields = ('id', 'name', 'color', 'slug')
        read_only_fields = fields


class IngredientSerializer(ModelSerializer):
    """Сериализатор для вывода ингридиентов."""
    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = fields


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

    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError(
                'Количество ингредиента должно быть больше нуля!'
            )
        return value


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
        queryset = IngredientAmount.objects.filter(recipe=obj).all()
        return IngredientAmountSerializer(queryset, many=True).data

    def get_presence(self, model, obj):
        user = request = self.context.get('request').user
        if user.is_anonymous:
            return False
        return model.objects.filter(user=user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.get_presence(Favorite, obj)

    def get_is_in_shopping_cart(self, obj):
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
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient=ingredient.get('id')
            ) for ingredient in ingredients_list
        ])

    def validate(self, data):
        ingredients = self.initial_data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise ValidationError(
                    'Ингредиенты должны быть уникальными!'
                )
            ingredients_list.append(ingredient_id)

        tags = data['tags']
        if not tags:
            raise ValidationError({
                'tags': 'Нужно выбрать хотя бы один тэг!'
            })
        tags_list = []
        for tag in tags:
            if tag in tags_list:
                raise ValidationError({
                    'tags': 'Тэги должны быть уникальными!'
                })
            tags_list.append(tag)

        cooking_time = data['cooking_time']
        if int(cooking_time) <= 0:
            raise ValidationError({
                'cooking_time': 'Время приготовления должно быть больше 0!'
            })
        return data

    def create_tags(self, tags, recipe):
        for tag in tags:
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

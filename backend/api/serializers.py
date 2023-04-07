from api.fields import Base64ImageField
from rest_framework.serializers import (
    CharField,
    IntegerField,
    ModelSerializer,
    PrimaryKeyRelatedField,
    SerializerMethodField,
    ValidationError,
)

from recipes.models import (
    Favoutrite,
    Ingredient,
    IngredientAmount,
    Recipe,
    Tag,
    ShoppingCart,
)
from users.serializers import CustomUserSerializer


class TagsSerialiser(ModelSerializer):
    """Сериализатор для вывода тегов."""
    class Meta:
        model = Tag
        fields = '__all__'
        read_only_fields = fields


class IngredientSerialiser(ModelSerializer):
    """Сериализатор для вывода ингридиентов."""
    class Meta:
        model = Ingredient
        fields = '__all__'
        read_only_fields = fields


class IngredientAmountSerialiser(ModelSerializer):
    """Сериализатор для вывода количества ингредиентов."""
    id = IntegerField(source='ingredient.id')
    name = CharField(source='ingredient.name')
    measurement_unit = CharField(source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'measurement_unit', 'amount')


class AddIngredientSerializer(ModelSerializer):
    """Сериализатор для добавления ингредиентов."""
    id = PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = IntegerField()

    class Meta:
        model = IngredientAmount
        fields = ('id', 'amount')
    
    def validate_amount(self, value):
        if value <= 0:
            raise ValidationError(
                'Количество ингридиентов не должно быть меньше или равно 0'
            )
        return value


class RecipeGetSerialiser(ModelSerializer):
    """Сериализатор для отображения рецептов."""
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerialiser(many=True)
    tags = TagsSerialiser(many=True, read_only=True)
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

    def get_presence(self, model, obj):
        request = self.context.get('request')
        if not request or request.user.is_anonymous:
            return False
        return model.objects.filter(user=request.user, recipe=obj).exists()

    def get_is_favorited(self, obj):
        return self.get_presence(Favoutrite, obj)

    def get_is_in_shopping_cart(self, obj):
        return self.get_presence(ShoppingCart, obj)


class ShortRecipeSerialiser(ModelSerializer):
    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')


class RecipeChangeSerialiser(ModelSerializer):
    tags = PrimaryKeyRelatedField(
        many=True, queryset=Tag.objects.all(),
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

    def validate(self, data):
        ingredients = data['ingredients']
        ingredients_list = []
        for ingredient in ingredients:
            ingredient_id = ingredient['id']
            if ingredient_id in ingredients_list:
                raise ValidationError({
                    'ingredients': 'Ингредиенты должны быть уникальными!'
                })
            ingredients_list.append(ingredient_id)
            amount = ingredient['amount']
            if int(amount) <= 0:
                raise ValidationError({
                    'amount': 'Количество ингредиента должно быть больше нуля!'
                })

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

    @staticmethod
    def add_ingredients(ingredients_list, recipe):
        IngredientAmount.objects.bulk_create([
            IngredientAmount(
                recipe=recipe,
                amount=ingredient.get('amount'),
                ingredient_id=ingredient.get('id')
            ) for ingredient in ingredients_list
        ])

    @staticmethod
    def add_tags(tags, recipe):
        for tag in tags:
            recipe.tags.add(tag)
    
    def create(self, validated_data):
        author = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        recipe = Recipe.objects.create(author=author, **validated_data)
        self.add_tags(tags, recipe)
        self.add_ingredients(ingredients, recipe)
        return recipe

    def to_representation(self, instance):
        request = self.context.get('request')
        context = {'request': request}
        return RecipeGetSerialiser(instance, context=context).data

    def update(self, instance, validated_data):
        instance.tags.clear()
        IngredientAmount.objects.filter(recipe=instance).delete()
        self.add_tags(validated_data.pop('tags'), instance)
        self.add_ingredients(validated_data.pop('ingredients'), instance)
        return super().update(instance, validated_data)




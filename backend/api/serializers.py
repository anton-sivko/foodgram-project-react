from rest_framework import serializers
from drf_extra_fields.fields import Base64ImageField
from users.models import Subscription, User
from recipes.models import Favorite, Ingredient, IngredientAmount, Recipe, ShoppingCart, Tag


class CustomUserSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True)
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'email', 'id', 'username', 'first_name',
            'last_name', 'password', 'is_subscribed'
        )
        write_only_fields = ('password',)

    def create(self, validated_data):
        """Создание нового пользователя."""
        user = User.objects.create(
            email=validated_data['email'],
            username=validated_data['username'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

    def get_is_subscribed(self, obj):
        """Статус подписки на автора."""
        user_id = self.context.get('request').user.id
        return Subscription.objects.filter(
            author=obj.id, user=user_id).exists()
    

class IngredientAmountSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField(
        source='ingredient.id')
    name = serializers.ReadOnlyField(
        source='ingredient.name')
    measurement_unit = serializers.ReadOnlyField(
        source='ingredient.measurement_unit')

    class Meta:
        model = IngredientAmount
        fields = ('id', 'name', 'amount', 'measurement_unit')


class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ('__all__')


class RecipeSerializer(serializers.ModelSerializer):
    author = CustomUserSerializer(read_only=True)
    ingredients = IngredientAmountSerializer(read_only=True, many=True,
                                             source='recipe')
    tags = TagSerializer(read_only=True, many=True)
    image = Base64ImageField()
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    def get_is_favorited(self, obj):
        user_id = self.context.get('request').user.id
        return Favorite.objects.filter(user=user_id,
                                       favorite_recipe=obj.id).exists()
    
    def get_is_in_shopping_cart(self, obj):
        user_id = self.context.get('request').user.id
        return ShoppingCart.objects.filter(user=user_id,
                                           recipe=obj.id).exists()

    class Meta:
        model = Recipe
        fields = ('id', 'tags', 'author', 'ingredients', 'is_favorited',
                  'is_in_shopping_cart', 'name', 'image', 'text',
                  'cooking_time')


class IngredientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ingredient
        fields = ('__all__')






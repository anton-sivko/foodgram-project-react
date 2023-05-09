from django_filters import ModelMultipleChoiceFilter
from django_filters.rest_framework import FilterSet, filters
from recipes.models import Ingredient, Recipe, Tag
from users.models import User


class RecipeFilter(FilterSet):
    tags = ModelMultipleChoiceFilter(field_name='tags__slug',
                                     to_field_name='slug',
                                     queryset=Tag.objects.all()
                                     )
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_favorited = filters.BooleanFilter(
        method='filter_in_favorite')
    is_in_shopping_cart = filters.BooleanFilter(
        method='filter_in_shopping_cart')

    def filter_in_favorite(self, queryset, name, value):
        if value:
            return queryset.filter(favorite_recipe__user=self.request.user)
        return queryset

    def filter_in_shopping_cart(self, queryset, name, value):
        if value:
            return queryset.filter(recipe_carts__user=self.request.user)
        return queryset

    class Meta:
        model = Recipe
        fields = ('tags', 'author')


class IngredientFilter(FilterSet):
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name',)

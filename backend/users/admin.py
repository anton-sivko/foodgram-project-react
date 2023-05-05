from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)

from .models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'is_active', 'username', 'password', 'email',
                    'first_name', 'last_name'
                    )
    fields = (
        ('is_active', ),
        ('username', 'email', ),
        ('password'),
        ('first_name', 'last_name', ),
    )
    fieldsets = []

    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )
    save_on_top = True


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')


@register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'author')
    fields = (
        'name', 'cooking_time', 'text', 'tags',
        'image', 'author', 'in_favorites'
    )
    readonly_fields = ('in_favorites',)
    list_filter = ('name', 'author', 'tags')

    @admin.display(description='В избранном')
    def in_favorites(self, obj):
        return obj.favorite_recipe.count()


@register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    list_filter = ('name', )
    search_fields = ('name', )


@register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    list_editable = ('name', 'color', 'slug')


@register(IngredientAmount)
class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    list_editable = ('recipe', 'ingredient', 'amount')


@register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'favorite_recipe')
    list_editable = ('user', 'favorite_recipe')


@register(ShoppingCart)
class ShoppingCartAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    list_editable = ('user', 'recipe')

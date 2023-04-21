from django.db import models
from users.models import User


class Ingredient(models.Model):
    pass


class Tag(models.Model):
    pass


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='Автор рецепта'
    )
    name = models.CharField(
        max_length=256,
        verbose_name='Название рецепта'
        )
    image = models.ImageField(
        upload_to='recipes/',
        null=True, blank=True
        )
    description = models.CharField(
        max_length=2000,
        verbose_name='Описание рецепта')
    ingredients = models.ManyToManyField(
        Ingredient,
        verbose_name='Ингредиенты',
        related_name='recipes'
        )
    tags = models.ManyToManyField(
        Tag,
        verbose_name='Тег рецепта',
        related_name='recipes'
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        default=0
    )
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True
        )

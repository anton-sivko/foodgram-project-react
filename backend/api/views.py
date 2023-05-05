from api.filters import RecipeFilter
from api.permissions import AdminOrAuthor_OrReadOnly
from django.db.models import Sum
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from djoser.views import UserViewSet
from recipes.models import (Favorite, Ingredient, IngredientAmount, Recipe,
                            ShoppingCart, Tag)
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)
from rest_framework.response import Response
from users.models import Subscription, User

from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeReadSerializer, RecipeShortSerializer,
                          RecipeWriteSerializer, SubscriptionSerializer,
                          TagSerializer)


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer

    @action(detail=True, methods=['post', 'delete'],
            url_path='subscribe', url_name='subscribe')
    def subscribe(self, request, pk):
        user = request.user
        author = get_object_or_404(User, pk=pk)
        if user == author:
            return Response({'errors': 'Подписаться на себя нельзя'},
                            status=status.HTTP_400_BAD_REQUEST)
        subscription = Subscription.objects.filter(
            user=user, author=author)
        if request.method == 'POST':
            if subscription.exists:
                return Response({'errors': 'Подписка уже существует'},
                                status=status.HTTP_400_BAD_REQUEST)
            queryset = Subscription.objects.create(user=user, author=author)
            serializer = SubscriptionSerializer(queryset,
                                                context={'request': request})
            serializer.is_valid(raise_exception=True)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            if not subscription.exists:
                return Response({'errors': 'Подписка отсутствует'},
                                status=status.HTTP_400_BAD_REQUEST)
            subscription.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=False, methods=['get'],
            url_path='subscriptions', url_name='subscriptions')
    def subscriptions(self, request):
        user = request.user
        queryset = user.follower.all()
        pages = self.paginate_queryset(queryset)
        serializer = SubscriptionSerializer(
            pages, many=True, context={'request': request})
        return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeWriteSerializer
    permission_classes = (IsAuthenticatedOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def get_serializer_class(self):
        if self.request.method in SAFE_METHODS:
            return RecipeReadSerializer
        return RecipeWriteSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    @action(detail=True, methods=['post', 'delete'],
            url_path='favorite', url_name='favorite')
    def favorite(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = RecipeShortSerializer(recipe, data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            if Favorite.objects.filter(user=user,
                                       recipe=recipe).exists():
                return Response({'errors': 'Рецепт уже добавлен в избранное.'},
                                status=status.HTTP_400_BAD_REQUEST)
            Favorite.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(Favorite, recipe=recipe, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=True, methods=['post', 'delete'],
            permission_classes=(IsAuthenticated,),
            url_path='shopping_cart', url_name='shopping_cart')
    def shopping_cart(self, request, pk=None):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user
        if request.method == 'POST':
            serializer = RecipeShortSerializer(recipe, data=request.data,
                                               context={'request': request})
            serializer.is_valid(raise_exception=True)
            if ShoppingCart.objects.filter(user=user, recipe=recipe):
                return Response({'errors': 'Рецепт уже добавлен в корзину'},
                                status=status.HTTP_400_BAD_REQUEST)
            ShoppingCart.objects.create(user=user, recipe=recipe)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        if request.method == 'DELETE':
            get_object_or_404(ShoppingCart, recipe=recipe, user=user).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)

    @action(detail=False, methods=['get'],
            permission_classes=(IsAuthenticated,),
            url_path='download_shopping_cart',
            url_name='download_shopping_cart')
    def download_shopping_cart(self, request, **kwargs):
        user = request.user
        file_name = 'Shopping_list.txt'
        shopping_list = []
        if not user.user_carts.exists():
            return Response(status=status.HTTP_400_BAD_REQUEST)
        ingredients = (IngredientAmount.objects.filter(
            recipe__recipe_carts__user=user)
            .values('ingredient__name', 'ingredient__measurement_unit')
            .annotate(amount=Sum('amount')))
        print(ingredients)
        for i in ingredients:
            print(i)
            shopping_list.append(f'{i["ingredient__name"]}: {i["amount"]}'
                                 f' {i["ingredient__measurement_unit"]}')
        response = HttpResponse(shopping_list,
                                content_type='text.txt; charset=utf-8')
        response['Content-Disposition'] = f'attachment; filename={file_name}'
        return response


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    permission_classes = (AdminOrAuthor_OrReadOnly,)
    pagination_class = None


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    permission_classes = (AdminOrAuthor_OrReadOnly,)
    pagination_class = None

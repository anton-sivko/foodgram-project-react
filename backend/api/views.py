from django.contrib.auth import get_user_model
from rest_framework import viewsets
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from django.shortcuts import render
from djoser.views import UserViewSet
from recipes.models import Ingredient, Recipe, Tag
from .serializers import (CustomUserSerializer, IngredientSerializer,
                          RecipeSerializer, TagSerializer,
                          )
from api.filters import RecipeFilter
from rest_framework.permissions import (SAFE_METHODS, IsAuthenticated,
                                        IsAuthenticatedOrReadOnly)


User = get_user_model()


class CustomUserViewSet(UserViewSet):
    queryset = User.objects.all()
    permission_classes = (IsAuthenticatedOrReadOnly,)
    serializer_class = CustomUserSerializer
    # def get_serializer_class(self):
    #     if self.action == 'set_password':
    #         return SetPasswordSerializer
    #     if self.action == 'create':
    #         return UserCreateSerializer
    #     return UserListSerializer

    # def get_permissions(self):
    #     if self.action == 'me':
    #         self.permission_classes = [IsAuthenticated]
    #     return super().get_permissions()

    # @action(detail=False, permission_classes=(IsAuthenticated,))
    # def subscriptions(self, request):
    #     queryset = Subscribe.objects.filter(user=request.user)
    #     pages = self.paginate_queryset(queryset)
    #     serializer = SubscribeSerializer(
    #         pages,
    #         many=True,
    #         context={'request': request},)
    #     return self.get_paginated_response(serializer.data)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    filter_backends = (DjangoFilterBackend,)
    filter_class = RecipeFilter

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer

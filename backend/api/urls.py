from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CustomUserViewSet, IngredientViewSet,
                    RecipeViewSet, TagViewSet)

app_name = 'api'

v1_router = DefaultRouter()

v1_router.register('users', CustomUserViewSet, 'users')
v1_router.register('recipes', RecipeViewSet, 'recipes')
v1_router.register('ingredients', IngredientViewSet, 'ingredients')
v1_router.register('tags', TagViewSet, 'tags')

# v1_router.register('genres', GenreViewSet)
# v1_router.register('categories', CategoryViewSet)
# v1_router.register('titles', TitleViewSet, basename='titles')
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews',
#     ReviewViewSet, basename='review')
# v1_router.register(
#     r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
#     CommentViewSet, basename='comment')

urlpatterns = [
    path('', include(v1_router.urls)),
    path('auth/', include('djoser.urls.authtoken')),
]

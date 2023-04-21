from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (CategoryViewSet, CommentViewSet, GenreViewSet,
                    ReviewViewSet, TitleViewSet, UserViewSet)

v1_router = DefaultRouter()

v1_router.register('users', UserViewSet)
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
    path('auth/', include('users.urls')),
]
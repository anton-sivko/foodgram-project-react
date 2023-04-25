from django.shortcuts import render
from djoser.views import UserViewSet as CustomUserViewSet


class UserViewSet(CustomUserViewSet):
    pass

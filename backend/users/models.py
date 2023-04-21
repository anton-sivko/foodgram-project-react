from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
    ]

    username = models.CharField(
        verbose_name='Логин',
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        validators=[UnicodeUsernameValidator],
        error_messages={
            'unique': "Пользователь с таким username уже существует",
        },
    )
    password = models.CharField(
        verbose_name='Пароль',
        max_length=settings.LIMIT_USERNAME,
    )

    is_active = models.BooleanField(
        verbose_name='Активирован',
        default=True,)

    email = models.EmailField(
        verbose_name='Адрес электронной почты',
        max_length=settings.LIMIT_EMAIL,
        unique=True,
        error_messages={
            'unique': "Пользователь с таким email уже существует",
        },
    )
    role = models.CharField(
        max_length=max(len(role) for role, _ in ROLE_CHOICES),
        choices=ROLE_CHOICES,
        default=USER
    )
    first_name = models.CharField(
        verbose_name='Имя',
        max_length=settings.LIMIT_USERNAME
    )

    last_name = models.CharField(
        verbose_name='Фамилия',
        max_length=settings.LIMIT_USERNAME
    )

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username

from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.db import models
from users.validators import username_me_denied


class User(AbstractUser):
    USER = 'user'
    ADMIN = 'admin'

    ROLE_CHOICES = [
        (USER, USER),
        (ADMIN, ADMIN),
    ]

    username = models.CharField(
        max_length=settings.LIMIT_USERNAME,
        unique=True,
        validators=[UnicodeUsernameValidator, username_me_denied],
        error_messages={
            'unique': "Пользователь с таким username уже существует",
        },
    )
    email = models.EmailField(
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
    first_name = models.CharField(max_length=settings.LIMIT_USERNAME,
                                  blank=True)
    bio = models.TextField(blank=True)

    @property
    def is_user(self):
        return self.role == self.USER

    @property
    def is_moderator(self):
        return self.role == self.MODERATOR

    @property
    def is_admin(self):
        return self.role == self.ADMIN or self.is_superuser or self.is_staff

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.username

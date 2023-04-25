from django.conf import settings
from rest_framework import serializers
from users.models import User
from rest_framework.validators import UniqueValidator


class UserSerializer(serializers.ModelSerializer):
    username = serializers.RegexField(
        max_length=settings.LIMIT_USERNAME,
        regex=r'^[\w.@+-]+\Z',
        validators=[UniqueValidator(
            queryset=User.objects.all(),
            message='Пользователь с таким username уже существует'
        )],
        required=True
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')
        read_only_fields = ('role',)

    # def validate_username(self, value):
    #     return username_me_denied(value)

    def validate_role(self, value):
        if value not in [User.ADMIN, User.USER, User.MODERATOR]:
            raise serializers.ValidationError(f"Несуществующая роль: {value}")
        return value

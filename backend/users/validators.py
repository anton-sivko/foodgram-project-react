from django.core import exceptions


def username_me_denied(value):
    if value.lower() == 'me':
        raise exceptions.ValidationError(
            'Имя пользователя "me" запрещено!'
        )
    return value

from django.contrib import admin
from django.contrib.admin import register
from django.contrib.auth.admin import UserAdmin
from users.models import Subscription, User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ('id', 'is_active', 'username', 'password', 'email',
                    'first_name', 'last_name'
                    )
    fields = (
        ('is_active', ),
        ('username', 'email', ),
        ('password'),
        ('first_name', 'last_name', ),
    )
    fieldsets = []

    search_fields = (
        'username', 'email',
    )
    list_filter = (
        'first_name', 'email',
    )
    save_on_top = True


@register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):
    list_display = ('pk', 'user', 'author')

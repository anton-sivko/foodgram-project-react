from django.contrib import admin
from django.contrib.admin import register
from .models import User


@register(User)
class UserAdmin(admin.ModelAdmin):
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
        'is_active', 'first_name', 'email',
    )
    save_on_top = True

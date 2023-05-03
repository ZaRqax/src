from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.models import Group

from .forms import CustomUserCreationForm
from .models import User


admin.site.unregister(Group)


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    list_display = (
        'username',
        'full_name',
        'email',
        'is_active',
        'is_superuser',
    )
    list_filter = ('is_active', 'is_superuser', 'created_at')
    list_display_links = ('email', 'username')
    search_fields = ('first_name', 'last_name', 'email', 'username')
    ordering = ('-id',)
    readonly_fields = ('created_at', 'updated_at', 'last_login')
    fieldsets = (
        (
            None,
            {
                'fields': ('username', 'email', 'password'),
            },
        ),
        (
            'Информация о пользователе',
            {'fields': ('first_name', 'last_name', 'middle_name')},
        ),
        (
            'Должность',
            {'fields': ('department', 'position')},
        ),
        (
            'Права пользователя',
            {'fields': ('is_active', 'is_superuser')},
        ),
        (
            'Системная информация',
            {'fields': ('created_at', 'updated_at', 'last_login')},
        ),
    )

    add_form = CustomUserCreationForm
    add_fieldsets = (
        (
            None,
            {'fields': ('username', 'email', 'password1', 'password2')},
        ),
        (
            'Информация о пользователе',
            {'fields': ('first_name', 'last_name', 'middle_name')},
        ),
        (
            'Должность',
            {'fields': ('department', 'position')},
        ),
        (
            'Права пользователя',
            {'fields': ('is_active', 'is_superuser')},
        ),
    )

    @admin.display(description='ФИО', ordering='last_name')
    def full_name(self, obj: User) -> str:
        return obj.full_name

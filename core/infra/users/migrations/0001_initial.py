# Generated by Django 4.1.5 on 2023-02-02 07:20

import django.contrib.auth.validators
from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("auth", "0012_alter_user_first_name_max_length"),
    ]

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("password", models.CharField(max_length=128, verbose_name="password")),
                (
                    "last_login",
                    models.DateTimeField(
                        blank=True, null=True, verbose_name="last login"
                    ),
                ),
                (
                    "is_superuser",
                    models.BooleanField(
                        default=False,
                        help_text="Designates that this user has all permissions without explicitly assigning them.",
                        verbose_name="superuser status",
                    ),
                ),
                (
                    "is_staff",
                    models.BooleanField(
                        default=False,
                        help_text="Designates whether the user can log into this admin site.",
                        verbose_name="staff status",
                    ),
                ),
                (
                    "date_joined",
                    models.DateTimeField(
                        default=django.utils.timezone.now, verbose_name="date joined"
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(
                        auto_now=True,
                        help_text="Поле будет изменено при обновлении любого из полей модели.",
                        null=True,
                        verbose_name="Дата последнего обновления",
                    ),
                ),
                (
                    "username",
                    models.CharField(
                        error_messages={
                            "unique": "Пользователь с таким username уже существует."
                        },
                        help_text="Обязательно для заполнения. 64 символа или меньше. Только буквы, цифры и @/./+/-/_.",
                        max_length=64,
                        unique=True,
                        validators=[
                            django.contrib.auth.validators.UnicodeUsernameValidator()
                        ],
                        verbose_name="Имя пользователя",
                    ),
                ),
                (
                    "first_name",
                    models.CharField(
                        help_text="Обязательно для заполнения. 64 символа или меньше.",
                        max_length=64,
                        verbose_name="Имя",
                    ),
                ),
                (
                    "last_name",
                    models.CharField(
                        help_text="Обязательно для заполнения. 64 символа или меньше.",
                        max_length=64,
                        verbose_name="Фамилия",
                    ),
                ),
                (
                    "middle_name",
                    models.CharField(
                        blank=True, default="", max_length=64, verbose_name="Отчество"
                    ),
                ),
                (
                    "email",
                    models.EmailField(
                        max_length=128, unique=True, verbose_name="E-mail пользователя"
                    ),
                ),
                (
                    "position",
                    models.CharField(max_length=256, verbose_name="Должность"),
                ),
                ("department", models.CharField(max_length=256, verbose_name="Отдел")),
                (
                    "is_active",
                    models.BooleanField(
                        default=True,
                        help_text="Указатель, что пользователь является активным. Уберите выделение, если хотите отключить аккаунт вместо удаления",
                        verbose_name="Активен в системе",
                    ),
                ),
                (
                    "groups",
                    models.ManyToManyField(
                        blank=True,
                        help_text="The groups this user belongs to. A user will get all permissions granted to each of their groups.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.group",
                        verbose_name="groups",
                    ),
                ),
                (
                    "user_permissions",
                    models.ManyToManyField(
                        blank=True,
                        help_text="Specific permissions for this user.",
                        related_name="user_set",
                        related_query_name="user",
                        to="auth.permission",
                        verbose_name="user permissions",
                    ),
                ),
            ],
            options={
                "verbose_name": "Пользователь",
                "verbose_name_plural": "Пользователи",
            },
        ),
    ]

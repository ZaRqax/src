from typing import (
    Any,
    TYPE_CHECKING,
)

from django.contrib.auth.base_user import BaseUserManager as _BaseUserManager
from django.utils.translation import gettext_lazy as _


if TYPE_CHECKING:
    from core.infra.users.models import User


class UserManager(_BaseUserManager):
    def create_user(self, *, email: str, password: str, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_active', True)

        if not email:
            raise ValueError(_('Email is required'))

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, *, username: str, email: str, password: str, **extra_fields: Any) -> 'User':
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))

        elif extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True'))

        return self.create_user(
            username=username,
            email=email,
            password=password,
            **extra_fields,
        )

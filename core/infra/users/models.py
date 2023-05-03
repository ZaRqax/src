from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.infra.models import BaseModel

from .managers import UserManager
from .validators import username_validator


class User(AbstractUser, BaseModel):
    username = models.CharField(
        _('Имя пользователя'),
        max_length=64,
        unique=True,
        help_text=_(
            'Обязательно для заполнения. 64 символа или меньше. Только буквы, цифры и @/./+/-/_.',
        ),
        validators=[username_validator],
        error_messages={
            'unique': _('Пользователь с таким username уже существует.'),
        },
    )

    first_name = models.CharField(
        max_length=64,
        verbose_name=_('Имя'),
        help_text=_(
            'Обязательно для заполнения. 64 символа или меньше.',
        ),
    )
    last_name = models.CharField(
        max_length=64,
        verbose_name=_('Фамилия'),
        help_text=_(
            'Обязательно для заполнения. 64 символа или меньше.',
        ),
    )
    middle_name = models.CharField(
        max_length=64,
        verbose_name=_('Отчество'),
        default='',
        blank=True,
    )
    email = models.EmailField(
        verbose_name=_('E-mail пользователя'),
        unique=True,
        max_length=128,
    )
    position = models.CharField(
        verbose_name=_('Должность'),
        max_length=256,
    )
    department = models.CharField(
        verbose_name=_('Отдел'),
        max_length=256,
    )
    is_active = models.BooleanField(
        verbose_name=_('Активен в системе'),
        default=True,
        help_text=_(
            'Указатель, что пользователь является активным. '
            'Уберите выделение, если хотите отключить аккаунт вместо удаления',
        ),
    )

    objects: UserManager = UserManager()

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.full_name

    @property
    def full_name(self) -> str:
        return f'{self.last_name} {self.first_name} {self.middle_name}'.strip()

    @property
    def short_name(self) -> str:
        """Last name and first name."""
        return f'{self.last_name} {self.first_name}'.strip()

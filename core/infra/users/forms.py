from django.contrib.auth.forms import (
    UserChangeForm as _UserChangeForm,
    UserCreationForm as _UserCreationForm,
)
from django.forms import (
    fields,
    Form,
)
from django.utils.translation import gettext_lazy as _

from .validators import (
    email_validator,
    username_validator,
)


class BaseUserForm(Form):
    username = fields.CharField(
        max_length=64,
        label=_('Имя пользователя'),
        validators=[username_validator],
    )
    email = fields.CharField(
        max_length=128,
        label=_('E-mail пользователя'),
        validators=[email_validator],
    )
    first_name = fields.CharField(
        max_length=64,
        label=_('Имя'),
    )
    last_name = fields.CharField(
        max_length=64,
        label=_('Фамилия'),
    )
    middle_name = fields.CharField(
        max_length=64,
        label=_('Отчество'),
        required=False,
        empty_value='',
    )
    department = fields.CharField(
        max_length=256,
        label=_('Отдел'),
    )
    position = fields.CharField(
        max_length=256,
        label=_('Должность'),
    )
    is_active = fields.BooleanField(
        initial=True,
        label=_('Активен в системе'),
        required=False,
        help_text=_('Пользователь может работать в системе'),
    )
    is_superuser = fields.BooleanField(
        initial=False,
        label=_('Администратор'),
        help_text=_('Указывает, что пользователь является администратором системы'),
        required=False,
    )


class CustomUserCreationForm(BaseUserForm, _UserCreationForm):
    ...


class CustomUserChangeForm(BaseUserForm, _UserChangeForm):
    ...

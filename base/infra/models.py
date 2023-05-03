from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_('Дата создания'),
    )
    updated_at = models.DateTimeField(
        verbose_name=_('Дата последнего обновления'),
        auto_now=True,
        null=True,
        blank=True,
        help_text=_('Поле будет изменено при обновлении любого из полей модели.'),
    )

    class Meta:
        abstract = True

from django.db import models
from django.utils.translation import gettext_lazy as _

from base.infra.models import BaseModel


class ValueType(BaseModel):
    title = models.CharField(
        _('Наименование'),
        max_length=64,
        unique=True,
    )

    class Meta:
        verbose_name = _('Тип')
        verbose_name_plural = _('Типы')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<TypeGrade(id={self.id!r}, title={self.title})>'

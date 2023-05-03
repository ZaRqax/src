from django.db import models
from django.utils.translation import gettext_lazy as _

from base.infra.models import BaseModel
from core.infra.attributes.models.querysets import AttributeQuerySet


class Attribute(BaseModel):
    title = models.CharField(
        _('Название атрибута'),
        max_length=256,
        unique=True,
    )
    measurement = models.ForeignKey(
        'attributes.MeasurementUnit',
        verbose_name=_('Единица измерения атрибута'),
        on_delete=models.PROTECT,
        related_name='attributes',
        null=True,
        blank=True,
    )
    value_type = models.ForeignKey(
        'catalogs.ValueType',
        verbose_name=_('Тип значения атрибута'),
        on_delete=models.PROTECT,
        related_name='attributes',
    )

    objects = AttributeQuerySet.as_manager()

    class Meta:
        verbose_name = _('Атрибут')
        verbose_name_plural = _('Атрибуты')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<Attribute(id={self.id!r}, title={self.title})>'


class AttributeValue(BaseModel):
    entity = models.ForeignKey(
        'entities.Entity',
        verbose_name=_('Объект'),
        on_delete=models.PROTECT,
        related_name='attribute_values',
    )
    attribute = models.ForeignKey(
        'attributes.Attribute',
        verbose_name=_('Атрибут'),
        on_delete=models.PROTECT,
        related_name='attribute_values',
    )
    value = models.TextField(
        _('Значения атрибута'),
    )


class MeasurementUnit(BaseModel):
    title = models.CharField(
        _('Название единицы измерения'),
        max_length=256,
        unique=True,
    )
    description = models.TextField(
        _('Описание единицы измерения'),
    )

    class Meta:
        verbose_name = _('Единица измерения')
        verbose_name_plural = _('Единицы измерения')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<MeasurementUnit(id={self.id!r}, title={self.title})>'

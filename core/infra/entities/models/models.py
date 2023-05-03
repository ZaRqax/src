from django.contrib.auth import get_user_model
from django.db import models
from django.utils.translation import gettext_lazy as _

from base.infra.models import BaseModel
from core.infra.entities.models.querysets import EntityQuerySet


User = get_user_model()


class Entity(BaseModel):
    title = models.CharField(
        _('Наименование объекта'),
        max_length=1024,
        unique=True,
    )
    parent = models.ForeignKey(
        'self',
        verbose_name=_('Родительский объект'),
        on_delete=models.PROTECT,
        related_name='children',
        null=True,
        blank=True,
    )
    type = models.ForeignKey(
        'entities.EntityType',
        verbose_name=_('Тип объекта'),
        on_delete=models.PROTECT,
        related_name='entities',
        null=True,
        blank=True,
    )
    creator = models.ForeignKey(
        User,
        verbose_name=_('Создатель'),
        on_delete=models.PROTECT,
        related_name='entities',
    )
    is_deleted = models.BooleanField(
        _('Признак удаленного объекта'),
        default=False,
    )
    attributes = models.ManyToManyField(
        'attributes.Attribute',
        verbose_name=_('Атрибуты'),
        through='attributes.AttributeValue',
        related_name='entities',
    )

    objects = EntityQuerySet.as_manager()

    class Meta:
        verbose_name = _('Объект')
        verbose_name_plural = _('Объекты')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<Entity(id={self.id!r}, title={self.title})>'


class EntityType(BaseModel):
    title = models.CharField(
        _('Название типа объекта'),
        max_length=1024,
        unique=True,
    )
    attributes = models.ManyToManyField(
        'attributes.Attribute',
        verbose_name=_('Атрибуты'),
        related_name='entity_types',
    )
    creator = models.ForeignKey(
        User,
        verbose_name=_('Создатель'),
        on_delete=models.PROTECT,
        related_name='entity_types',
        null=True,
        blank=True,
    )
    grade = models.ForeignKey(
        'entities.TypeGrade',
        verbose_name=_('Грейд типа объекта'),
        on_delete=models.PROTECT,
        related_name='entity_types',
        null=True,
        blank=True,
    )

    class Meta:
        verbose_name = _('Тип объекта')
        verbose_name_plural = _('Типы объектов')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<EntityType(id={self.id!r}, title={self.title})>'


class TypeGrade(BaseModel):
    title = models.CharField(
        _('Название объекта'),
        max_length=1024,
        unique=True,
    )
    parents = models.ManyToManyField(
        'self',
        verbose_name=_('Родительский объект'),
        symmetrical=False,
        related_name='children',
        blank=True,
    )

    class Meta:
        verbose_name = _('Грейд типа объекта')
        verbose_name_plural = _('Грейды типов объектов')

    def __str__(self):
        return self.title

    def __repr__(self) -> str:
        return f'<TypeGrade(id={self.id!r}, title={self.title})>'

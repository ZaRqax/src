from import_export.fields import Field
from import_export.resources import ModelResource

from core.infra.entities.models import Entity


class EntityResource(ModelResource):
    title = Field(attribute='title', column_name='Наименование')
    type_title = Field(attribute='type__title', column_name='Тип объекта')
    parent_title = Field(attribute='parent__title', column_name='Родительский объект')

    class Meta:
        model = Entity
        fields = ('title', 'type_title', 'parent_title')

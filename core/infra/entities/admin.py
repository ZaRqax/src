from django.contrib import admin

from core.infra.common.admin import ReadOnlyModelAdmin
from core.infra.entities.models import (
    Entity,
    TypeGrade,
)


class AttributeValueInline(admin.TabularInline):
    model = Entity.attributes.through
    classes = ('collapse',)
    fields = (
        'attribute',
        'value',
    )


@admin.register(Entity)
class EntityAdmin(ReadOnlyModelAdmin):
    list_display = (
        'title',
        'creator_full_name',
        'is_deleted',
    )
    list_select_related = ('creator',)
    inlines = [AttributeValueInline]

    @admin.display(description='Создатель')
    def creator_full_name(self, obj):
        return obj.creator.full_name


@admin.register(TypeGrade)
class TypeGradeAdmin(admin.ModelAdmin):
    list_display = ('title',)
    filter_horizontal = ('parents',)

from django.contrib import admin

from core.infra.attributes.models import (
    Attribute,
    MeasurementUnit,
)


@admin.register(Attribute)
class AttributeAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'measurement_title',
        'value_type_title',
    )
    search_fields = ('title',)
    list_select_related = (
        'measurement',
        'value_type',
    )

    @admin.display(description='Единица измерения')
    def measurement_title(self, obj):
        return getattr(obj.measurement, 'title', None)

    @admin.display(description='Тип значения')
    def value_type_title(self, obj):
        return obj.value_type.title


@admin.register(MeasurementUnit)
class MeasurementUnitAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)

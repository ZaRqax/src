from django_filters import rest_framework as drf_filters

from core.infra.entities.constants import ENTITIES_ORDERING_FIELDS
from core.infra.entities.models import Entity


class EntitiesFilter(drf_filters.FilterSet):
    ordering = drf_filters.OrderingFilter(fields=ENTITIES_ORDERING_FIELDS)

    title = drf_filters.CharFilter(lookup_expr='icontains')
    parent_title = drf_filters.CharFilter(
        lookup_expr='icontains',
        field_name='parent__title',
    )
    type_title = drf_filters.CharFilter(
        lookup_expr='icontains',
        field_name='type__title',
    )

    class Meta:
        model = Entity
        fields = ()

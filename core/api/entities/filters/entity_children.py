from django_filters import rest_framework as drf_filters

from core.infra.entities.constants import ENTITY_CHILDREN_ORDERING_FIELDS
from core.infra.entities.models import Entity


class EntityChildrenFilter(drf_filters.FilterSet):
    order_by = drf_filters.OrderingFilter(fields=ENTITY_CHILDREN_ORDERING_FIELDS)

    class Meta:
        model = Entity
        fields = ()

from django.db import models
from django.db.models import (
    Prefetch,
    Q,
)

from core.infra.attributes.repositories.attribute import attribute_read_repository


class EntityQuery:
    @staticmethod
    def deleted() -> Q:
        return Q(is_deleted=True)


class EntityQuerySet(models.QuerySet):
    def with_parent(self):
        return self.select_related('parent')

    def with_type_grade(self):
        return self.select_related('type__grade')

    def with_creator(self):
        return self.select_related('creator')

    def with_attributes(self):
        attributes_qs = attribute_read_repository.get_many().with_all_relations().with_values()
        return self.prefetch_related(Prefetch('attributes', queryset=attributes_qs))

    def with_all_relations(self):
        return self.with_parent().with_type_grade().with_creator().with_attributes()

from django.db import models
from django.db.models import Prefetch


class AttributeQuerySet(models.QuerySet):
    def with_measurement(self):
        from core.infra.attributes.repositories.measurement_unit import measurement_unit_read_repository

        measurement_qs = measurement_unit_read_repository.get_many()
        return self.prefetch_related(Prefetch('measurement', queryset=measurement_qs))

    def with_value_type(self):
        return self.select_related('value_type')

    def with_all_relations(self):
        return self.with_measurement().with_value_type()

    def with_values(self):
        return self.annotate(value=models.F('attribute_values__value'))

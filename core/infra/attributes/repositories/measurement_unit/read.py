from django.db.models import QuerySet

from base.infra.repositories import BaseReadRepository as _BaseReadRepository
from core.infra.attributes.models import MeasurementUnit


class MeasurementUnitReadRepository(_BaseReadRepository):
    model = MeasurementUnit

    def get_one(self, pk: int) -> MeasurementUnit | None:
        return self.db.filter(id=pk).first()

    def get_many(self) -> QuerySet[MeasurementUnit]:
        return self.db.all()

    def get_count(self) -> int:
        return self.db.count()

    def exists(self, pk: int) -> bool:
        return self.db.filter(id=pk).exists()

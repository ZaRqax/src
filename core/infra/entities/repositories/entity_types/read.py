from django.db.models import QuerySet

from base.infra.repositories import BaseReadRepository as _BaseReadRepository
from core.infra.entities.models import EntityType


class EntityTypeReadRepository(_BaseReadRepository):
    model = EntityType

    def get_one(self, pk: int) -> EntityType | None:
        return self.db.filter(id=pk).first()

    def get_many(self) -> QuerySet[EntityType]:
        return self.db.all()

    def get_count(self) -> int:
        return self.db.count()

    def exists(self, pk: int) -> bool:
        return self.db.filter(id=pk).exists()

from django.db.models import QuerySet

from base.infra.repositories import BaseReadRepository
from core.infra.entities.models import (
    Entity,
    TypeGrade,
)
from core.infra.entities.models.querysets import (
    EntityQuery,
    EntityQuerySet,
)


class EntityReadRepository(BaseReadRepository):
    model = Entity

    def get_one(self, pk: int) -> Entity | None:
        return self.db.filter(id=pk).first()

    def get_many(self) -> EntityQuerySet:
        return self.db.all()

    def get_count(self) -> int:
        return self.db.count()

    def exists(self, pk: int) -> bool:
        return self.db.filter(id=pk).exists()

    def filter_by_pk(self, pk: int) -> EntityQuerySet:
        return self.db.filter(id=pk)

    def get_by_type_grades(self, type_grades: QuerySet[TypeGrade]) -> EntityQuerySet:
        return self.db.filter(type__in=type_grades.values('entity_types')).select_related('type').order_by('pk')

    def get_entity_children(self, entity_id: int) -> QuerySet[Entity]:
        return self.db.filter(parent__in=self.db.filter(pk=entity_id))

    def get_undeleted(self) -> EntityQuerySet:
        return self.db.filter(~EntityQuery.deleted())

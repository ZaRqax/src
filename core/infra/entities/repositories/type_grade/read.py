from django.db.models import QuerySet

from base.infra.repositories import BaseReadRepository as _BaseReadRepository
from core.infra.entities.models import TypeGrade


class TypeGradeReadRepository(_BaseReadRepository):
    model = TypeGrade

    def get_one(self, pk: int) -> TypeGrade | None:
        return self.db.filter(id=pk).first()

    def get_many(self) -> QuerySet[TypeGrade]:
        return self.db.all()

    def exists(self, pk: int) -> bool:
        return self.db.exists()

    def get_count(self) -> int:
        return self.db.count()

    def get_parents_by_entity_type(self, entity_type_id: int) -> QuerySet[TypeGrade]:
        return self.db.filter(children__in=self.db.filter(entity_types=entity_type_id)).all()

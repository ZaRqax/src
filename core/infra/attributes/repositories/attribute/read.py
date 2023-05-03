from base.infra.repositories import BaseReadRepository as _BaseReadRepository
from core.infra.attributes.models import Attribute
from core.infra.attributes.models.querysets import AttributeQuerySet


class AttributeReadRepository(_BaseReadRepository):
    model = Attribute

    def get_one(self, pk: int) -> Attribute | None:
        return self.db.filter(id=pk).first()

    def get_many(self) -> AttributeQuerySet:
        return self.db.all()

    def get_count(self) -> int:
        return self.db.count()

    def get_by_entity_type(self, entity_type_id: int) -> AttributeQuerySet:
        return self.db.filter(entity_types=entity_type_id).with_all_relations()

    def exists(self, pk: int) -> bool:
        return self.db.filter(id=pk).exists()

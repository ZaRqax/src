from base.infra.repositories import BaseWriteRepository
from core.infra.attributes.models import AttributeValue
from core.infra.utils.repositories.constants import DEFAULT_CREATE_BATCH_SIZE


class AttributeValueWriteRepository(BaseWriteRepository):
    model = AttributeValue

    def create_one(self, entity_id: int, attribute_id: int, value: str) -> AttributeValue:
        return self.db.create(entity_id=entity_id, attribute_id=attribute_id, value=value)

    def create_many(
        self,
        attribute_values: list[AttributeValue],
        batch_size: int = DEFAULT_CREATE_BATCH_SIZE,
        ignore_conflicts: bool = False,
    ) -> list[AttributeValue]:
        return self.db.bulk_create(attribute_values, batch_size=batch_size, ignore_conflicts=ignore_conflicts)

    def update_one(self, pk: int, entity_id: int, attribute_id: int, value: str) -> AttributeValue:
        return self.db.filter(id=pk).update(entity_id=entity_id, attribute_id=attribute_id, value=value)

    def delete_one(self, pk: int) -> None:
        self.db.filter(id=pk).delete()

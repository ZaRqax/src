from base.infra.repositories import BaseWriteRepository as _BaseWriteRepository
from core.infra.model_example.models import (
    Attribute,
    Unit,
)


class AttributeWriteRepository(_BaseWriteRepository):
    model = Attribute

    def create_record(self, title: str, object: Unit, is_active: bool = True) -> Unit:
        return self.db.create(title=title, object=object, is_active=is_active)

    def update_record(self, pk: int, title: str, object: Unit, is_active: bool) -> Unit:
        return self.db.filter(id=pk).update(title=title, object=object, is_active=is_active)

    def delete_record(self, pk: int) -> None:
        self.db.objects.filter(id=pk).delete()

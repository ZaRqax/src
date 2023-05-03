from base.infra.repositories import BaseWriteRepository
from core.infra.entities.models import Entity


class EntityWriteRepository(BaseWriteRepository):
    model = Entity

    def create_one(
        self,
        title: str,
        creator_id: int,
        is_deleted: bool = False,
        parent_id: int | None = None,
        type_id: int | None = None,
    ) -> Entity:
        return self.db.create(
            title=title,
            creator_id=creator_id,
            is_deleted=is_deleted,
            parent_id=parent_id,
            type_id=type_id,
        )

    def update_one(
        self,
        pk: int,
        title: str,
        creator_id: int,
        is_deleted: bool = False,
        parent_id: int | None = None,
        type_id: int | None = None,
    ) -> Entity:
        return self.db.filter(id=pk).update(
            title=title,
            creator_id=creator_id,
            is_deleted=is_deleted,
            parent_id=parent_id,
            type_id=type_id,
        )

    def delete_one(self, pk: int) -> None:
        self.db.filter(id=pk).delete()

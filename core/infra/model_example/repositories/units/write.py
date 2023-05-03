from base.infra.repositories import BaseWriteRepository as _BaseWriteRepository
from core.infra.model_example.models import Unit
from core.infra.users.models import User


class UnitWriteRepository(_BaseWriteRepository):
    model = Unit

    def create_one(self, *, user: User, title: str, description: str, is_active: bool = True) -> Unit:
        return self.db.create(user=user, title=title, description=description, is_active=is_active)

    def update_one(self, pk: int, *, user: User, title: str, description: str, is_active: bool) -> Unit:
        return self.db.filter(id=pk).update(user=user, title=title, description=description, is_active=is_active)

    def delete_one(self, pk: int) -> None:
        self.db.filter(id=pk).delete()

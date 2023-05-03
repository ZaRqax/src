from django.db.models import QuerySet

from base.infra.repositories import BaseReadRepository as _BaseReadRepository
from core.infra.model_example.models import Unit
from core.infra.users.models import User


class UnitReadRepository(_BaseReadRepository):
    model = Unit

    def get_one(self, pk: int) -> Unit | None:
        try:
            return self.db.get(id=pk)
        except Unit.DoesNotExist:
            return None

    def get_count(self) -> int:
        return self.db.count()

    def get_many(self) -> QuerySet[Unit]:  # Нужны ли тут offset и limit?
        return self.db.all()

    def get_many_by_author(self, user: User) -> QuerySet[Unit]:
        return self.db.filter(user=user)

    def exists(self, pk: int) -> bool:
        return self.db.filter(id=pk).exists()

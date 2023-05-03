from dataclasses import dataclass

from base.domain.usecases import BaseUseCase
from core.domain.model_example.permissions import InitiatorMustBeActive
from core.domain.model_example.rules import (
    IRule,
    UnitMustBeActive,
)
from core.infra.model_example.models import Unit
from core.infra.model_example.repositories import UnitWriteRepository
from core.infra.users.models import User


@dataclass(frozen=True, kw_only=True)
class CreateUnit(BaseUseCase):
    user: User
    title: str
    description: str
    is_active: bool

    def permissions(self) -> list[IRule]:
        return [
            InitiatorMustBeActive(self.initiator),
        ]

    def rules(self) -> list[IRule]:
        return [
            UnitMustBeActive(self.is_active),
        ]

    def action(self) -> Unit:
        return UnitWriteRepository().create_one(
            user=self.user,
            title=self.title,
            description=self.description,
            is_active=self.is_active,
        )

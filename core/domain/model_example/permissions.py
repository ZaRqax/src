from dataclasses import dataclass

from base.domain.rules import DomainPermission
from core.infra.users.models import User


@dataclass(frozen=True)
class InitiatorMustBeActive(DomainPermission):
    value: User

    def is_correct(self) -> bool:
        return self.value and self.value.is_active

    def get_error_message(self) -> str:
        return 'Инициатор должен быть активен'

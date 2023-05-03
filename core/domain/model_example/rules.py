from dataclasses import dataclass

from base.domain.rules import (
    DomainRule,
    IRule,
)


@dataclass(frozen=True)
class UnitMustBeActive(DomainRule, IRule):
    value: bool

    def is_correct(self) -> bool:
        return self.value is True

    def get_error_message(self) -> str:
        return 'Объект должен быть активным, сейчас неактивен'

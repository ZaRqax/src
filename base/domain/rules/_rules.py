import abc
from dataclasses import dataclass
from typing import (
    NoReturn,
    Protocol,
)

from base.domain.exceptions import (
    BusinessLogicException,
    BusinessRuleTypeException,
    DomainPermissionException,
    DomainRuleException,
)


rule_dataclass = dataclass(frozen=True, kw_only=True)


@rule_dataclass
class IRule(Protocol):
    _exception_type: type[BusinessLogicException]

    def get_error_message(self) -> str:
        ...

    def is_correct(self) -> bool:
        ...

    def check(self) -> None:
        ...

    def get_exception(self) -> Exception:
        ...

    def raise_exception(self) -> NoReturn:
        ...


@rule_dataclass
class Rule(IRule, abc.ABC):
    """Бизнес-правило, описывающее определенное поведение.

    Поведение:
    - Может содержать входящие поля
    - Не должно меняться после его создания
    - Относится исключительно бизнес-процессам (не путать с валидацией)

    В чем валидация принципиально отличается от валидации: в валидации решения принимает разработчик,
    а в бизнес-правилах - заказчик.

    """

    _exception_type: type[BusinessLogicException] = BusinessLogicException

    @abc.abstractmethod
    def get_error_message(self) -> str:
        """Сообщение нарушенного правила."""
        ...

    @abc.abstractmethod
    def is_correct(self) -> bool:
        """Условие, при котором правило соблюдено."""
        ...

    def check(self) -> None:
        """Проверка соблюдения правила.

        Если не соблюдено - вызывает ошибку нарушенного правила.

        """

        if not self.is_correct():
            self.raise_exception()

    def get_exception(self) -> Exception:
        """Ошибка нарушенного правила."""

        return self._exception_type(self.get_error_message())

    def raise_exception(self) -> NoReturn:
        """Вызов ошибки нарушенного правила."""
        raise self.get_exception()


@rule_dataclass
class DomainRule(Rule, abc.ABC):
    _exception_type: type[BusinessLogicException] = DomainRuleException


@rule_dataclass
class DomainPermission(Rule, abc.ABC):
    _exception_type: type[BusinessLogicException] = DomainPermissionException


def check_rules(rules: list[IRule]) -> None:
    """Проверка набора правил."""

    for rule in rules:
        if not isinstance(rule, Rule):
            raise BusinessRuleTypeException(f'Expected "BusinessRule", gotten "{type(rule)}"')

        rule.check()

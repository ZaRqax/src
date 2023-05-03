import abc
from dataclasses import dataclass
from typing import Callable

from django.db import transaction

from core.infra.users.models import User

from .rules import check_rules


@dataclass(frozen=True)
class BaseUseCase(abc.ABC):
    """Описание бизнес-логики.

    # TODO: Если найдется кейс с чтением данных через UseCase - обсудить.

    """

    initiator: User | None

    # Список Permissions (бизнес-права)
    def permissions(self) -> list:
        return []

    # Список Rules (бизнес-правила)
    def rules(self) -> list:
        """Возвращает бизнес-правила, необходимые для проверки возможности
        выполнения бизнес-сценария."""
        return []

    @abc.abstractmethod
    def action(self) -> None:
        """Выполняет непосредственные действия сценария.

        Например, создать/изменить/удалить объект.

        """

        raise NotImplementedError

    @transaction.atomic
    def execute(self):
        """Выполняет проверку прав и валидацию правил бизнес-логики.

        Если проверки прошли, то выполняет сценарий. Иными словами
        данный метод вызывает по порядку все методы описанные выше.

        """

        check_rules(self.permissions())
        check_rules(self.rules())

        return self.action()


IUseCaseFactory = Callable[[dict], BaseUseCase]

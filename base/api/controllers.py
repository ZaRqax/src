import abc
from typing import Any

from base.domain.usecases import BaseUseCase


class BaseUseCaseController(abc.ABC):
    """Базовый контроллер для работы с UseCase."""

    _use_case: BaseUseCase

    @property
    def use_case(self) -> BaseUseCase:
        return self._use_case

    @abc.abstractmethod
    def execute(self) -> Any:
        """Выполнение сценария из UseCase."""
        ...

    @abc.abstractmethod
    def _init_use_case(self, validated_data: dict) -> None:
        """Инициализация UseCase."""
        ...

    @abc.abstractmethod
    def _validate(self) -> None:
        """Выполняет валидацию в UseCase."""
        ...

    @abc.abstractmethod
    def _check_permissions(self) -> None:
        """Выполняет проверку прав в UseCase."""
        ...

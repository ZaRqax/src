import abc
from typing import Any

from django.db import models


class IRepository(metaclass=abc.ABCMeta):
    """Репозиторий-интерфейс для всех репозиториев.

    Не должен содержать никакой логики, только перечень общих методов.

    """

    @property
    @abc.abstractmethod
    def db(self) -> Any:
        ...


class IReadRepository(IRepository, metaclass=abc.ABCMeta):
    """Репозиторий-интерфейс, отвечающий за чтение данных из БД.

    Не должен содержать никакой логики, только перечень общих методов.
    Может быть напрямую вызван в API.

    """

    @abc.abstractmethod
    def get_one(self, identifier):
        ...

    @abc.abstractmethod
    def get_many(self):
        ...

    @abc.abstractmethod
    def get_count(self) -> int:
        ...

    @abc.abstractmethod
    def exists(self, pk: int) -> bool:
        ...


class IWriteRepository(IRepository, metaclass=abc.ABCMeta):
    """Репозиторий, отвечающий за запись данных в БД.

    Не должен содержать никакой логики, только перечень общих методов.
    Не может быть напрямую вызван в API (только через слой бизнес-
    логики).

    """

    @abc.abstractmethod
    def create_one(self, **kwargs):
        ...

    @abc.abstractmethod
    def update_one(self, **kwargs):
        ...

    @abc.abstractmethod
    def delete_one(self, identifier):
        ...


class DjangoMixin:
    model: models.Model = NotImplemented

    @property
    def db(self):
        return self.model.objects  # type: ignore[attr-defined]


class BaseWriteRepository(DjangoMixin, IWriteRepository, metaclass=abc.ABCMeta):
    ...


class BaseReadRepository(DjangoMixin, IReadRepository, metaclass=abc.ABCMeta):
    ...

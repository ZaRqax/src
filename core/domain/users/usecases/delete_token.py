from dataclasses import dataclass

from rest_framework_simplejwt.exceptions import (
    InvalidToken,
    TokenError,
)
from rest_framework_simplejwt.tokens import RefreshToken

from base.domain.rules import IRule
from base.domain.usecases import BaseUseCase
from core.domain.users.constants import INVALID_REFRESH_TOKEN_ERROR


@dataclass(frozen=True, kw_only=True)
class DeleteToken(BaseUseCase):
    """Добавление токена в blacklist при выходе из сессии."""

    refresh_token: str

    def permissions(self) -> list[IRule]:
        return []

    def rules(self) -> list[IRule]:
        return []

    def action(self) -> None:
        try:
            RefreshToken(self.refresh_token).blacklist()
        except TokenError:
            raise InvalidToken(INVALID_REFRESH_TOKEN_ERROR)

        return None

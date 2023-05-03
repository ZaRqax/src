from dataclasses import dataclass

from rest_framework_simplejwt.tokens import RefreshToken

from base.domain.rules import IRule
from base.domain.usecases import BaseUseCase
from core.infra.users.models import User


@dataclass(frozen=True, kw_only=True)
class CreateToken(BaseUseCase):
    """Создание токенов."""

    user: User

    def permissions(self) -> list[IRule]:
        return []

    def rules(self) -> list[IRule]:
        return []

    def action(self) -> RefreshToken:
        refresh_token = RefreshToken.for_user(self.user)
        return refresh_token

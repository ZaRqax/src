import typing as t

from rest_framework.test import APIClient

import pytest

from core.domain.users.usecases.create_token import CreateToken
from core.infra.conftest import *  # noqa
from core.infra.users.models import User


class CustomApiClient(APIClient):
    _user: t.Optional[User] = None
    _access_token: str = ''
    _refresh_token: str = ''

    @property
    def user(self) -> t.Optional[User]:
        return self._user

    @property
    def access_token(self) -> str:
        return self._access_token

    @property
    def refresh_token(self) -> str:
        return self._refresh_token

    def authorize_by_token(self, access_token: str) -> None:
        self.credentials(HTTP_AUTHORIZATION=f'Bearer {access_token}')

    def authorize(self, user: User) -> 'CustomApiClient':
        self.logout()

        token = CreateToken(
            initiator=user,
            user=user,
        ).execute()

        self._refresh_token = str(token)
        self._access_token = str(token.access_token)

        self.authorize_by_token(self.access_token)
        self._user = user

        return self


@pytest.fixture
def unauthorized_api_client() -> CustomApiClient:
    return CustomApiClient()


@pytest.fixture
def authorized_api_client(user: User) -> CustomApiClient:
    return CustomApiClient().authorize(user)

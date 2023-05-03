from functools import wraps
from typing import Any

from rest_framework import exceptions
from rest_framework.serializers import BaseSerializer

from base.api.controllers import BaseUseCaseController
from base.domain.exceptions import (
    DomainPermissionException,
    DomainRuleException,
)
from base.domain.rules import check_rules
from base.domain.usecases import IUseCaseFactory


class ViewUseCaseController(BaseUseCaseController):
    def __init__(self, use_case_factory: IUseCaseFactory, serializer: BaseSerializer | None = None):
        self._serializer = serializer
        self._use_case_factory = use_case_factory

    def execute(self) -> Any:

        validated_data = {}

        if self._serializer:
            self._serializer.is_valid(raise_exception=True)
            validated_data = self._serializer.validated_data

        self._init_use_case(validated_data)

        self._check_permissions()
        self._validate()

        return self._use_case.action()

    def _init_use_case(self, validated_data: dict) -> None:
        self._use_case = self._use_case_factory(validated_data)

    def _validate(self) -> None:
        try:
            check_rules(self._use_case.rules())
        except DomainRuleException as ex:
            raise exceptions.ValidationError(detail=str(ex))

    def _check_permissions(self) -> None:
        try:
            check_rules(self._use_case.permissions())
        except DomainPermissionException as ex:
            raise exceptions.PermissionDenied(detail=str(ex))


def catch_use_case_errors_as_view(method):
    """Decorator to handle UseCase Exception when using in ViewSet actions and
    covert it to DRF Exceptions."""

    @wraps(method)
    def wrapper(request, *args, **kwargs):
        try:
            return method(request, *args, **kwargs)
        except DomainRuleException as ex:
            raise exceptions.ValidationError(detail=str(ex))
        except DomainPermissionException as ex:
            raise exceptions.PermissionDenied(detail=str(ex))

    return wrapper

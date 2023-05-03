from rest_framework import serializers
from rest_framework.fields import CharField

from drf_spectacular.utils import OpenApiResponse


class BadRequestResponse(serializers.Serializer):
    message = serializers.CharField()
    extra = serializers.DictField(
        child=CharField(),
        default={},
    )


UnauthorizedResponse = OpenApiResponse(
    description='Пользователь не авторизован',
    response=BadRequestResponse,
)

NotFoundResponse = OpenApiResponse(
    description='Не найдено',
    response=BadRequestResponse,
)

from typing import Any

from rest_framework import serializers


SerializerFields = dict[str, serializers.Field]


def create_serializer_class(name: str, fields: SerializerFields) -> type[serializers.Serializer]:
    """Create serializer class dynamically."""

    return type(name, (serializers.Serializer,), fields)  # noqa


def inline_serializer(
    name: str,
    fields: SerializerFields,
    data: dict | None = None,
    **kwargs: Any,
) -> serializers.Serializer:
    """Create serializer class dynamically and return serializer instance.

    Usage:
        >>> from rest_framework import serializers
        >>> from base.api.serializers import inline_serializer
        >>>
        >>> class EntitySerializer(serializers.Serializer):  # noqa
        >>>     user = inline_serializer(fields={
        >>>         "id": serializers.IntegerField(),
        >>>         "username": serializers.CharField(),
        >>>     })
        >>>     attributes = inline_serializer(fields={
        >>>         "id": serializers.IntegerField(),
        >>>         "title": serializers.CharField(),
        >>>     }, many=True)
        >>>     is_active = serializers.BooleanField()
        >>>     created_at = serializers.DateTimeField()

    """

    serializer_class = create_serializer_class(name=name, fields=fields)

    if data is not None:
        return serializer_class(data=data, **kwargs)

    return serializer_class(**kwargs)

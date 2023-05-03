from rest_framework import (
    serializers,
    status,
)
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.api.common.openapi_serializers import (
    NotFoundResponse,
    UnauthorizedResponse,
)
from core.infra.attributes.repositories.attribute import attribute_read_repository
from core.infra.entities.models import EntityType


class TypeAttributesApiView(APIView):
    class GetTypeAttributesResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        measurement = serializers.CharField(source='measurement.title', allow_null=True)
        value_type = serializers.CharField(source='value_type.title')

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='getTypeAttributes',
        description='Метод по получению атрибутов типа объекта',
        summary='GetTypeAttributes',
        responses={
            status.HTTP_200_OK: GetTypeAttributesResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    def get(self, request, pk):
        get_object_or_404(EntityType, id=pk)
        attributes = attribute_read_repository.get_by_entity_type(pk)

        out_serializer = self.GetTypeAttributesResponseSerializer(attributes, many=True)

        return Response(out_serializer.data)

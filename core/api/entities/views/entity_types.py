from rest_framework import (
    serializers,
    status,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.api.common.openapi_serializers import UnauthorizedResponse
from core.infra.entities.repositories.entity_types import entity_type_read_repository


class EntityTypesApiView(APIView):
    class GetEntityTypesResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='getEntityTypes',
        description='Метод по получению списка типов объектов',
        summary='GetEntityTypes',
        responses={
            status.HTTP_200_OK: GetEntityTypesResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
        },
    )
    def get(self, request, *args, **kwargs):
        entity_types = entity_type_read_repository.get_many()
        out_serializer = self.GetEntityTypesResponseSerializer(entity_types, many=True)

        return Response(out_serializer.data)

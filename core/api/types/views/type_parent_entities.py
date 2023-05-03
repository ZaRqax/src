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
from core.infra.entities.models import EntityType
from core.infra.entities.repositories.entities import entity_read_repository
from core.infra.entities.repositories.type_grade.read import TypeGradeReadRepository


class ParentEntitiesTypeView(APIView):
    class GetTypeParentsResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()
        type = serializers.CharField(source='type.title')

    permission_classes = [IsAuthenticated]

    @extend_schema(
        operation_id='getParentEntitiesType',
        description='Метод по получению атрибутов типа объекта',
        summary='GetParentEntitiesType',
        responses={
            status.HTTP_200_OK: GetTypeParentsResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    def get(self, request, pk):
        get_object_or_404(EntityType, id=pk)
        parent_type_grades = TypeGradeReadRepository().get_parents_by_entity_type(pk)
        entities = entity_read_repository.get_by_type_grades(parent_type_grades)

        out_serializer = self.GetTypeParentsResponseSerializer(entities, many=True)

        return Response(out_serializer.data)

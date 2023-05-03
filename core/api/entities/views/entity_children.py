from rest_framework import (
    serializers,
    status,
)
from rest_framework.generics import get_object_or_404
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from drf_spectacular.utils import extend_schema

from core.api.common.mixins import FilterAPIMixin
from core.api.common.openapi_serializers import (
    NotFoundResponse,
    UnauthorizedResponse,
)
from core.api.entities.filters.entity_children import EntityChildrenFilter
from core.infra.entities.models import Entity
from core.infra.entities.repositories.entities import entity_read_repository


class EntityChildrenApiView(FilterAPIMixin, LimitOffsetPagination, APIView):  # type: ignore
    class GetEntityChildrenResponseSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField()

    permission_classes = [IsAuthenticated]
    filterset_class = EntityChildrenFilter

    @extend_schema(
        operation_id='getEntityChildren',
        description='Метод по получению дочерних объектов',
        summary='GetEntityChildren',
        responses={
            status.HTTP_200_OK: GetEntityChildrenResponseSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    def get(self, request, pk):
        get_object_or_404(Entity, id=pk)
        entity_children = self.filter_queryset(entity_read_repository.get_entity_children(pk))
        results = self.paginate_queryset(entity_children, request, view=self)

        out_serializer = self.GetEntityChildrenResponseSerializer(results, many=True)

        return self.get_paginated_response(out_serializer.data)

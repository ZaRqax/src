from django.http import HttpResponse
from django.utils import timezone
from drf_excel.renderers import XLSXRenderer

from rest_framework import (
    serializers,
    status,
)
from rest_framework.decorators import renderer_classes
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet

from drf_spectacular.utils import extend_schema

from base.api.serializers import inline_serializer
from core.api.common.mixins import FilterAPIMixin
from core.api.common.openapi_serializers import (
    NotFoundResponse,
    UnauthorizedResponse,
)
from core.api.controllers import catch_use_case_errors_as_view
from core.api.entities.filters.entities import EntitiesFilter
from core.domain.entities.usecases.create_entity import CreateEntityUseCase
from core.domain.entities.usecases.delete_entity import DeleteEntityUseCase
from core.infra.attributes.models import AttributeValue
from core.infra.attributes.repositories.attribute import attribute_read_repository
from core.infra.entities.constants import XLSX_FILE_NAME
from core.infra.entities.models import Entity
from core.infra.entities.repositories.entities import entity_read_repository
from core.infra.entities.repositories.entity_types import entity_type_read_repository
from core.infra.entities.resourses import EntityResource


class EntityViewSet(FilterAPIMixin, ViewSet):
    class CreateEntitySerializer(serializers.Serializer):
        title = serializers.CharField(max_length=1024)
        type = serializers.PrimaryKeyRelatedField(queryset=entity_type_read_repository.get_many())
        parent = serializers.PrimaryKeyRelatedField(
            required=False,
            queryset=entity_read_repository.get_many(),  # type: ignore
        )
        attributes = serializers.ListSerializer(
            required=False,
            child=inline_serializer(
                'CreateEntityAttributeSerializer',
                fields={
                    'id': serializers.PrimaryKeyRelatedField(queryset=attribute_read_repository.get_many()),
                    'value': serializers.CharField(max_length=1024),
                },
            ),
        )

    class EntitySerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=1024)
        type = inline_serializer(
            'EntityEntityTypeSerializer',
            fields={
                'id': serializers.IntegerField(),
                'title': serializers.CharField(max_length=1024),
            },
        )
        parent = inline_serializer(
            'EntityEntityParentSerializer',
            required=False,
            fields={
                'id': serializers.IntegerField(),
                'title': serializers.CharField(max_length=1024),
                'type': serializers.CharField(max_length=1024, source='type.title'),
            },
        )
        creator = inline_serializer(
            'EntityEntityCreatorSerializer',
            fields={
                'id': serializers.IntegerField(),
                'last_name': serializers.CharField(max_length=64),
                'first_name': serializers.CharField(max_length=64),
                'middle_name': serializers.CharField(
                    max_length=64,
                    required=False,
                    allow_null=True,
                ),
            },
        )
        attributes = serializers.ListSerializer(
            required=False,
            child=inline_serializer(
                'EntityAttributeSerializer',
                fields={
                    'id': serializers.IntegerField(),
                    'title': serializers.CharField(max_length=1024),
                    'value': serializers.CharField(max_length=1024),
                    'measurement': serializers.CharField(max_length=256, source='measurement.title', allow_null=True),
                    'value_type': serializers.CharField(max_length=64, source='value_type.title'),
                },
            ),
        )

    class EntityListSerializer(serializers.Serializer):
        id = serializers.IntegerField()
        title = serializers.CharField(max_length=1024)
        parent = inline_serializer(
            'EntityEntityParentSerializer',
            required=False,
            fields={
                'id': serializers.IntegerField(),
                'title': serializers.CharField(max_length=1024),
            },
        )
        type = inline_serializer(
            'EntityEntityTypeSerializer',
            required=False,
            fields={
                'id': serializers.IntegerField(),
                'title': serializers.CharField(max_length=1024),
            },
        )
        creator = inline_serializer(
            'EntityEntityCreatorSerializer',
            fields={
                'id': serializers.IntegerField(),
                'full_name': serializers.CharField(max_length=256),
            },
        )

    permission_classes = []
    filterset_class = EntitiesFilter

    @extend_schema(
        operation_id='createEntity',
        description='Метод по созданию объекта',
        request=CreateEntitySerializer,
        summary='CreateEntity',
        responses={
            status.HTTP_201_CREATED: EntitySerializer,
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
        },
    )
    @catch_use_case_errors_as_view
    def create(self, request, *args, **kwargs):
        in_serializer = self.CreateEntitySerializer(data=request.data)
        in_serializer.is_valid(raise_exception=True)

        use_case = CreateEntityUseCase(
            initiator=request.user,
            title=in_serializer.validated_data['title'],
            type=in_serializer.validated_data['type'],
            creator=request.user,
            parent=in_serializer.validated_data.get('parent'),
            attribute_values=[
                AttributeValue(attribute=attribute['id'], value=attribute['value'])
                for attribute in in_serializer.validated_data.get('attributes', [])
            ],
        )

        entity = use_case.execute()
        entity = entity_read_repository.filter_by_pk(entity.pk).with_all_relations().first()
        out_serializer = self.EntitySerializer(instance=entity)

        return Response(out_serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(
        operation_id='getEntity',
        description='Метод по получению информации об объекте',
        summary='Get Entity',
        responses={
            status.HTTP_200_OK: EntitySerializer,
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    def retrieve(self, request, pk, *args, **kwargs):
        get_object_or_404(Entity, id=pk)
        entity = entity_read_repository.filter_by_pk(pk).with_all_relations().first()
        out_serializer = self.EntitySerializer(instance=entity)
        return Response(out_serializer.data)

    @extend_schema(
        operation_id='getEntities',
        description='Метод по получению списка объектов',
        summary='Get Entities',
        responses={
            status.HTTP_200_OK: EntityListSerializer(many=True),
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    def list(self, request, *args, **kwargs):
        entities = self.filter_queryset(entity_read_repository.get_undeleted().with_all_relations().order_by('pk'))
        out_serializer = self.EntityListSerializer(entities, many=True)
        response: HttpResponse | Response = Response(out_serializer.data)
        if request.META.get('HTTP_ACCEPT') == 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet':
            dataset = EntityResource().export(entities)
            response = HttpResponse(content=dataset.xlsx, content_type='application/vnd.ms-excel')
            now = timezone.now()
            response['Content-Disposition'] = (
                f'attachment; ' f'filename={XLSX_FILE_NAME.format(date=now.strftime("%Y:%m:%d_%H:%M:%S"))}'
            )

        return response

    @extend_schema(
        operation_id='deleteEntity',
        description='Метод для удаления обьекта',
        summary='Delete Entity',
        responses={
            status.HTTP_200_OK: {},
            status.HTTP_401_UNAUTHORIZED: UnauthorizedResponse,
            status.HTTP_404_NOT_FOUND: NotFoundResponse,
        },
    )
    @catch_use_case_errors_as_view
    def delete(self, request, pk, *args, **kwargs):
        entity = get_object_or_404(Entity, id=pk)
        use_case = DeleteEntityUseCase(
            initiator=request.user,
            entity=entity,
        )
        use_case.execute()

        return Response(status=status.HTTP_200_OK)

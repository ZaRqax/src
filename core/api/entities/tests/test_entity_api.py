from io import BytesIO
from typing import Final

from rest_framework import status

import openpyxl
import pytest
from model_bakery import random_gen

from core.api.common.tests.urls import (
    entities_url,
    entity_detail_url,
)
from core.api.entities.views.entities import EntityViewSet
from core.infra.baker_recipes import entities_recipes
from core.infra.entities.repositories.entities import entity_read_repository


ATTRIBUTES_COUNT: Final[int] = 5
ENTITY_TITLE_MAX_LENGTH: int = entity_read_repository.model._meta.get_field('title').max_length
ENTITIES_COUNT: Final[int] = 5


def test_create_entity_api(authorized_api_client, entity_with_attributes):
    entity = entities_recipes.entity.prepare(parent=entity_with_attributes, _save_related=True)
    attributes = [
        entities_recipes.attribute_value.prepare(entity=entity, attribute=entities_recipes.attribute.make())
        for _ in range(ATTRIBUTES_COUNT)
    ]

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity.type_id,
            'parent': entity.parent_id,
            'attributes': [
                {
                    'id': attribute.attribute_id,
                    'value': attribute.value,
                }
                for attribute in attributes
            ],
        },
    )

    json_data = response.json()
    assert response.status_code == status.HTTP_201_CREATED, response.content

    expected_result = EntityViewSet.EntitySerializer(
        instance=entity_read_repository.filter_by_pk(json_data['id']).with_all_relations().first(),
    ).data

    assert json_data == expected_result, json_data
    assert len(json_data['attributes']) == ATTRIBUTES_COUNT


def test_create_entity_api_without_not_required_fields(authorized_api_client, entity):
    entity = entities_recipes.entity.prepare(parent=entity, _save_related=True)

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity.type_id,
        },
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED, response.content

    expected_result = EntityViewSet.EntitySerializer(
        instance=entity_read_repository.filter_by_pk(json_data['id']).with_all_relations().first(),
    ).data

    assert json_data == expected_result, json_data


def test_create_entity_api_with_attributes_without_measurement(authorized_api_client, entity_with_attributes):
    entity = entities_recipes.entity.prepare(_save_related=True)
    attributes = [
        entities_recipes.attribute_value.prepare(
            entity=entity,
            attribute=entities_recipes.attribute.make(measurement=None),
        )
        for _ in range(ATTRIBUTES_COUNT)
    ]

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity.type_id,
            'attributes': [
                {
                    'id': attribute.attribute_id,
                    'value': attribute.value,
                }
                for attribute in attributes
            ],
        },
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_201_CREATED, response.content

    entity = entity_read_repository.filter_by_pk(json_data['id']).with_all_relations().first()
    expected_result = {
        'id': entity.id,
        'title': entity.title,
        'type': {
            'id': entity.type.id,
            'title': entity.type.title,
        },
        'parent': None,
        'creator': {
            'id': entity.creator.id,
            'last_name': entity.creator.last_name,
            'first_name': entity.creator.first_name,
            'middle_name': entity.creator.middle_name,
        },
        'attributes': [
            {
                'id': attribute.id,
                'title': attribute.title,
                'value': attribute.value,
                'measurement': None,
                'value_type': attribute.value_type.title,
            }
            for attribute in entity.attributes.all()
        ],
    }

    assert json_data == expected_result, json_data


def test_create_entity_api_parent_does_not_exists(authorized_api_client):
    entity_type = entities_recipes.entity_type.make()
    parent = random_gen.gen_integer(1000, 5000)

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity_type.id,
            'parent': parent,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
    error_message = response.json()['extra']['fields']['parent'][0]

    assert str(parent) in error_message


def test_create_entity_api_type_does_not_exists(authorized_api_client, entity_with_attributes):
    entity_type = random_gen.gen_integer(1000, 5000)

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity_type,
            'parent': entity_with_attributes.id,
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content
    error_message = response.json()['extra']['fields']['type'][0]

    assert str(entity_type) in error_message


def test_create_entity_api_attribute_does_not_exists(authorized_api_client, entity_with_attributes):
    entity = entities_recipes.entity.prepare(parent=entity_with_attributes, _save_related=True)

    response = authorized_api_client.post(
        entities_url(),
        data={
            'title': random_gen.gen_string(ENTITY_TITLE_MAX_LENGTH),
            'type': entity.type_id,
            'parent': entity.parent_id,
            'attributes': [
                {
                    'id': random_gen.gen_integer(1000, 5000),
                    'value': random_gen.gen_string(10),
                }
                for _ in range(ATTRIBUTES_COUNT)
            ],
        },
    )

    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.content


def test_get_entity_api(authorized_api_client, entity_with_attributes):
    response = authorized_api_client.get(entity_detail_url(entity_with_attributes.pk))

    json_data = response.json()
    assert response.status_code == status.HTTP_200_OK, response.content

    expected_result = EntityViewSet.EntitySerializer(
        instance=entity_read_repository.filter_by_pk(entity_with_attributes.pk).with_all_relations().first(),
    ).data

    assert json_data == expected_result, json_data


def test_get_entity_api_not_found(authorized_api_client):
    response = authorized_api_client.get(entity_detail_url(random_gen.gen_integer(1000, 5000)))

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.content


def test_get_entities_api(authorized_api_client):
    entities_recipes.entity.make(
        is_deleted=False,
        _quantity=ENTITIES_COUNT,
    )

    response = authorized_api_client.get(entities_url())

    assert response.status_code == status.HTTP_200_OK, response.content

    entities = entity_read_repository.get_undeleted().with_all_relations().order_by('pk')
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': {
                'id': entity.parent_id,
                'title': entity.parent.title,
            }
            if entity.parent
            else None,
            'type': {
                'id': entity.type_id,
                'title': entity.type.title,
            },
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        }
        for entity in entities
    ]
    json_data = response.json()

    assert json_data == expected_result, json_data


@pytest.mark.skip(reason='Не правильно работают заголовки')
def test_get_entities_api_response_file(authorized_api_client):
    entities_recipes.entity.make(
        is_deleted=False,
        _quantity=ENTITIES_COUNT,
    )
    headers = {'HTTP_ACCEPT': 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'}
    response = authorized_api_client.get(entities_url(), headers=headers)
    workbook_xml = BytesIO(response.content)
    workbook_xml.seek(0)
    wb = openpyxl.load_workbook(filename=workbook_xml)
    assert wb.active['A1'].value == 'Наименование'
    assert wb.active['B1'].value == 'Тип объекта'
    assert wb.active['C1'].value == 'Родительский объект'
    assert len(list(wb.active.rows)) == ENTITIES_COUNT + 1


def test_get_entities_api_empty_result(authorized_api_client):
    entities_recipes.entity.make(
        _quantity=ENTITIES_COUNT,
        is_deleted=True,
    )

    response = authorized_api_client.get(entities_url())

    assert response.status_code == status.HTTP_200_OK, response.content
    assert entity_read_repository.get_count() == ENTITIES_COUNT

    json_data = response.json()

    assert not json_data


def test_get_entities_api_without_not_required_fields(authorized_api_client):
    entities_recipes.entity.make(
        _quantity=ENTITIES_COUNT,
        is_deleted=False,
        type=None,
        parent=None,
    )

    response = authorized_api_client.get(entities_url())

    assert response.status_code == status.HTTP_200_OK, response.content

    entities = entity_read_repository.get_undeleted().with_all_relations().order_by('pk')
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': None,
            'type': None,
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        }
        for entity in entities
    ]
    json_data = response.json()

    assert json_data == expected_result, json_data


def test_get_entities_api_unauthorized(unauthorized_api_client):
    response = unauthorized_api_client.get(entities_url())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content


@pytest.mark.parametrize(
    'ordering',
    (
        'title',
        '-title',
        'parent__title',
        '-parent__title',
        'type__title',
        '-type__title',
    ),
)
def test_get_entities_api_with_ordering(authorized_api_client, ordering):
    first_entity = entities_recipes.entity.make(
        type=entities_recipes.entity_type.make(),
        is_deleted=False,
    )
    entities_recipes.entity.make(
        type=entities_recipes.entity_type.make(),
        parent=first_entity,
        is_deleted=False,
    )

    response = authorized_api_client.get(
        entities_url(),
        {
            'ordering': ordering,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.content

    entities = entity_read_repository.get_many().order_by(ordering)
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': {
                'id': entity.parent_id,
                'title': entity.parent.title,
            }
            if entity.parent
            else None,
            'type': {
                'id': entity.type_id,
                'title': entity.type.title,
            },
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        }
        for entity in entities
    ]
    json_data = response.json()

    assert json_data == expected_result, json_data


def test_get_entities_api_filter_by_title(authorized_api_client, entity):
    entity.title = 'suitable_title'
    entity.parent = None
    entity.type = None
    entity.save()
    entities_recipes.entity.make(_quantity=ENTITIES_COUNT, title='123')

    response = authorized_api_client.get(
        entities_url(),
        data={
            'title': entity.title,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_count = 1
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': None,
            'type': None,
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        },
    ]
    json_data = response.json()

    assert len(json_data) == expected_count, json_data
    assert entity_read_repository.get_count() > expected_count
    assert json_data == expected_result, json_data


def test_get_entities_api_filter_by_parent_title(authorized_api_client, entity):
    unsuitable_parent = entities_recipes.entity.make(title='123')
    entity.parent = entities_recipes.entity.make(title='suitable_title')
    entity.type = None
    entity.save()
    entities_recipes.entity.make(_quantity=ENTITIES_COUNT, parent=unsuitable_parent)

    response = authorized_api_client.get(
        entities_url(),
        data={
            'parent_title': entity.parent.title,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_count = 1
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': {
                'id': entity.parent_id,
                'title': entity.parent.title,
            },
            'type': None,
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        },
    ]
    json_data = response.json()

    assert len(json_data) == expected_count, json_data
    assert entity_read_repository.get_count() > expected_count
    assert json_data == expected_result, json_data


def test_get_entities_api_filter_by_type_title(authorized_api_client, entity):
    unsuitable_type = entities_recipes.entity_type.make(title='123')
    entity.parent = None
    entity.type = entities_recipes.entity_type.make(title='suitable_title')
    entity.save()
    entities_recipes.entity.make(_quantity=ENTITIES_COUNT, type=unsuitable_type)

    response = authorized_api_client.get(
        entities_url(),
        data={
            'type_title': entity.type.title,
        },
    )

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_count = 1
    expected_result = [
        {
            'id': entity.id,
            'title': entity.title,
            'parent': None,
            'type': {
                'id': entity.type_id,
                'title': entity.type.title,
            },
            'creator': {
                'id': entity.creator_id,
                'full_name': entity.creator.full_name,
            },
        },
    ]
    json_data = response.json()

    assert len(json_data) == expected_count, json_data
    assert entity_read_repository.get_count() > expected_count
    assert json_data == expected_result, json_data


def test_delete_entity_api(authorized_api_client, entity):
    assert not entity.is_deleted

    response = authorized_api_client.delete(entity_detail_url(entity.pk))

    assert response.status_code == status.HTTP_200_OK, response.content

    entity.refresh_from_db()

    assert entity.is_deleted


def test_delete_entity_api_not_found(authorized_api_client):
    nonexistent_id = 77777
    response = authorized_api_client.delete(entity_detail_url(nonexistent_id))
    assert response.status_code == status.HTTP_404_NOT_FOUND

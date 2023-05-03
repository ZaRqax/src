from rest_framework import status

from core.api.common.tests.urls import parent_entities_type_url
from core.api.types.views.type_parent_entities import ParentEntitiesTypeView
from core.infra.baker_recipes import entities_recipes
from core.infra.entities.models import EntityType


ENTITIES_COUNT = 5


def test_success_get_parent_entities_type(authorized_api_client, entity_type, type_grade):
    parent_type_grades = entities_recipes.type_grade.make(_quantity=ENTITIES_COUNT)
    type_grade.parents.set(parent_type_grades)
    entity_type.grade = type_grade
    entity_type.save()

    entity_types = entities_recipes.entity_type.make(_quantity=ENTITIES_COUNT, grade=iter(parent_type_grades))

    entities = entities_recipes.entity.make(_quantity=ENTITIES_COUNT, type=iter(entity_types))

    response = authorized_api_client.get(
        parent_entities_type_url(entity_type_id=entity_type.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_result = ParentEntitiesTypeView.GetTypeParentsResponseSerializer(
        entities,
        many=True,
    ).data

    assert json_data == expected_result, json_data


def test_success_empty_response(authorized_api_client, entity_type):
    response = authorized_api_client.get(
        parent_entities_type_url(entity_type_id=entity_type.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert not json_data


def test_entity_type_not_found(authorized_api_client):
    entity_type_id = 100

    assert not EntityType.objects.filter(pk=entity_type_id).exists()

    response = authorized_api_client.get(
        parent_entities_type_url(entity_type_id=entity_type_id),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.content


def test_unauthorized(unauthorized_api_client, entity_type):
    response = unauthorized_api_client.get(
        parent_entities_type_url(entity_type_id=entity_type.pk),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
    assert response.json().get('message')

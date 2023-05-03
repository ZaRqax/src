from rest_framework import status

from core.api.common.tests.urls import entity_types_url
from core.api.entities.views.entity_types import EntityTypesApiView
from core.infra.baker_recipes import entities_recipes
from core.infra.entities.repositories.entity_types.read import EntityTypeReadRepository


ENTITY_TYPES_COUNT = 10


def test_success_get_entity_types_api(authorized_api_client):
    entities_recipes.entity_type.make(_quantity=ENTITY_TYPES_COUNT)

    response = authorized_api_client.get(entity_types_url())

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_result = EntityTypesApiView.GetEntityTypesResponseSerializer(
        instance=EntityTypeReadRepository().get_many(),
        many=True,
    ).data

    assert json_data == expected_result, json_data


def test_unauthorized(unauthorized_api_client):
    response = unauthorized_api_client.get(entity_types_url())

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
    assert response.json().get('message')

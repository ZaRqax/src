from rest_framework import status

from core.api.common.tests.urls import type_attributes_url
from core.api.types.views.type_attributes import TypeAttributesApiView
from core.infra.entities.models import EntityType


def test_success_get_type_attributes(authorized_api_client, entity_type_with_attributes):
    response = authorized_api_client.get(
        type_attributes_url(entity_type_id=entity_type_with_attributes.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert len(json_data) == entity_type_with_attributes.attributes.count()

    expected_result = TypeAttributesApiView.GetTypeAttributesResponseSerializer(
        entity_type_with_attributes.attributes,
        many=True,
    ).data

    assert json_data == expected_result, json_data


def test_type_attributes_without_measurement(authorized_api_client, entity_type_with_attributes):
    entity_type_with_attributes.attributes.update(measurement=None)

    response = authorized_api_client.get(
        type_attributes_url(entity_type_id=entity_type_with_attributes.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_result = [
        {
            'id': attr.id,
            'title': attr.title,
            'measurement': None,
            'value_type': attr.value_type.title,
        }
        for attr in entity_type_with_attributes.attributes.all()
    ]

    assert json_data == expected_result, json_data


def test_entity_type_not_found(authorized_api_client):
    entity_type_id = 100

    assert not EntityType.objects.filter(pk=entity_type_id).exists()

    response = authorized_api_client.get(
        type_attributes_url(entity_type_id=entity_type_id),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.content


def test_unauthorized(unauthorized_api_client, entity_type):
    response = unauthorized_api_client.get(
        type_attributes_url(entity_type_id=entity_type.pk),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
    assert response.json().get('message')

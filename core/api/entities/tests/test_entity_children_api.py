from rest_framework import status

from core.api.common.tests.urls import entity_children_url
from core.api.entities.views.entity_children import EntityChildrenApiView
from core.infra.baker_recipes import entities_recipes
from core.infra.entities.models import Entity


ENTITY_CHILDREN_COUNT = 5


def test_success_get_entity_children(authorized_api_client, entity):
    entity.children.set(entities_recipes.entity.make(_quantity=ENTITY_CHILDREN_COUNT))

    response = authorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content

    expected_result = EntityChildrenApiView.GetEntityChildrenResponseSerializer(
        entity.children,
        many=True,
    ).data

    assert json_data['results'] == expected_result, json_data


def test_sort_created_at_asc(authorized_api_client, entity):
    first_child_entity = entities_recipes.entity.make(
        parent=entity,
    )
    entities_recipes.entity.make(
        parent=entity,
    )

    response = authorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
        data={
            'order_by': 'created_at',
        },
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert json_data['results'][0]['id'] == first_child_entity.pk


def test_sort_created_at_desc(authorized_api_client, entity):
    entities_recipes.entity.make(
        parent=entity,
    )
    second_child_entity = entities_recipes.entity.make(
        parent=entity,
    )

    response = authorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
        data={
            'order_by': '-created_at',
        },
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert json_data['results'][0]['id'] == second_child_entity.pk


def test_limit_entities(authorized_api_client, entity):
    limit_count = 1
    entity.children.set(entities_recipes.entity.make(_quantity=ENTITY_CHILDREN_COUNT))

    response = authorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
        data={
            'limit': limit_count,
        },
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert len(json_data['results']) == limit_count


def test_success_empty_response(authorized_api_client, entity):
    response = authorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
    )

    json_data = response.json()

    assert response.status_code == status.HTTP_200_OK, response.content
    assert not json_data['results']


def test_entity_not_found(authorized_api_client):
    entity_id = 1

    assert not Entity.objects.filter(pk=entity_id).exists()

    response = authorized_api_client.get(
        entity_children_url(entity_id=entity_id),
    )

    assert response.status_code == status.HTTP_404_NOT_FOUND, response.content


def test_unauthorized(unauthorized_api_client, entity):
    response = unauthorized_api_client.get(
        entity_children_url(entity_id=entity.pk),
    )

    assert response.status_code == status.HTTP_401_UNAUTHORIZED, response.content
    assert response.json().get('message')

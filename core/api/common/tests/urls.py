from django.urls import reverse


def login_url() -> str:
    return reverse('token:auth')


def logout_url() -> str:
    return reverse('token:logout')


def refresh_token_url() -> str:
    return reverse('token:refresh')


def type_attributes_url(entity_type_id: int) -> str:
    return reverse('types:type_attributes', kwargs={'pk': entity_type_id})


def entity_types_url() -> str:
    return reverse('entities:get_types')


def parent_entities_type_url(entity_type_id: int) -> str:
    return reverse('types:parent_entities', kwargs={'pk': entity_type_id})


def entity_children_url(entity_id: int) -> str:
    return reverse('entities:entity_children', kwargs={'pk': entity_id})


def entities_url() -> str:
    return reverse('entities:entities')


def entity_detail_url(pk: int) -> str:
    return reverse('entities:entity-detail', kwargs={'pk': pk})

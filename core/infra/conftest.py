import pytest

from core.infra.baker_recipes import (
    entities_recipes,
    users_recipes,
)
from core.infra.entities.models import (
    Entity,
    EntityType,
    TypeGrade,
)
from core.infra.users.models import User


@pytest.fixture
def user() -> User:
    """Пользователь."""
    return users_recipes.user.make()


@pytest.fixture
def entity_type() -> EntityType:
    """Тип объекта."""
    return entities_recipes.entity_type.make()


@pytest.fixture
def entity_type_with_attributes() -> EntityType:
    """Тип объекта с аттрибутами."""
    return entities_recipes.entity_type.make(make_m2m=True)


@pytest.fixture
def type_grade() -> TypeGrade:
    """Грейд типа объекта."""
    return entities_recipes.type_grade.make()


@pytest.fixture
def entity_with_attributes() -> Entity:
    entity = entities_recipes.entity.make()
    entities_recipes.attribute_value.make(entity=entity, _quantity=3, _bulk_create=True)
    return entity


@pytest.fixture
def entity() -> Entity:
    """Объект."""
    return entities_recipes.entity.make()

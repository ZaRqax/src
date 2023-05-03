from model_bakery.recipe import (
    foreign_key,
    Recipe,
    related,
    seq,
)

from core.infra.attributes.models import (
    Attribute,
    AttributeValue,
    MeasurementUnit,
)
from core.infra.users.baker_recipes import user

from .models import (
    Entity,
    EntityType,
    TypeGrade,
)


type_grade = Recipe(
    TypeGrade,
    title=seq('Название #'),
)

measurement_unit = Recipe(
    MeasurementUnit,
    title=seq('Название единицы измерения #'),
)

attribute = Recipe(
    Attribute,
    title=seq('Название атрибута #'),
    measurement=foreign_key(measurement_unit),
)

entity_type = Recipe(
    EntityType,
    title=seq('Название типа #'),
    grade=foreign_key(type_grade),
    attributes=related(attribute),
)

entity = Recipe(
    Entity,
    title=seq('Название объекта #'),
    type=foreign_key(entity_type),
    creator=foreign_key(user),
)

attribute_value = Recipe(
    AttributeValue,
    value=seq('Значения атрибута #'),
    attribute=foreign_key(attribute),
    entity=foreign_key(entity),
)

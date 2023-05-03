from dataclasses import dataclass

from django.contrib.auth import get_user_model

from base.domain.usecases import BaseUseCase
from core.infra.attributes.models import AttributeValue
from core.infra.attributes.repositories.attribute_values import attribute_value_write_repository
from core.infra.entities.models import (
    Entity,
    EntityType,
)
from core.infra.entities.repositories.entities import entity_write_repository


User = get_user_model()


@dataclass(frozen=True, kw_only=True)
class CreateEntityUseCase(BaseUseCase):
    title: str
    type: EntityType
    creator: User  # type: ignore
    parent: Entity | None = None
    attribute_values: list[AttributeValue] | None = None

    def action(self) -> Entity:
        entity = entity_write_repository.create_one(
            title=self.title,
            type_id=self.type.id,
            creator_id=self.creator.id,  # type: ignore
            parent_id=getattr(self.parent, 'id', None),
        )

        if not self.attribute_values:
            return entity

        for attribute_value in self.attribute_values:
            attribute_value.entity = entity

        attribute_value_write_repository.create_many(self.attribute_values)

        return entity

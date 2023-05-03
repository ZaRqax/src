from dataclasses import dataclass

from base.domain.usecases import BaseUseCase
from core.infra.entities.models import Entity


@dataclass(frozen=True, kw_only=True)
class DeleteEntityUseCase(BaseUseCase):
    entity: Entity

    def action(self) -> None:
        if not self.entity.is_deleted:
            self.entity.is_deleted = True
            self.entity.save()

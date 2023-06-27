from abc import ABC, abstractmethod
from typing import Optional

import shortuuid

from app.application.badge.badge_command_model import BadgeCreateModel, BadgeCreateResponse
from app.domain.badge.model.badge import Badge
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.school import School
from app.domain.user.repository.user_repository import UserRepository


class BadgeCommandUseCase(ABC):
    """BadgeCommandUseCase defines a command usecase inteface related Badge entity."""

    @abstractmethod
    def create(self, data: BadgeCreateModel) -> BadgeCreateResponse:
        raise NotImplementedError


class BadgeCommandUseCaseImpl(BadgeCommandUseCase):
    """BadgeCommandUseCaseImpl implements a command usecases related Badge entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            badge_repository: BadgeRepository,
            school_repository: SchoolRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository
        self.badge_repository: BadgeRepository = badge_repository

    def create(self, data: BadgeCreateModel) -> BadgeCreateResponse:
        try:
            school = self.school_repository.find_by_id(data.school_id)

            uuid = shortuuid.uuid()

            badge = Badge(
                is_default=data.is_default,
                uuid=uuid,
                name=data.name,
                icon=data.icon,
                school=School(name=school.name, id=school.id),
                description=data.description,
                is_secret=data.is_secret
            )

            self.badge_repository.create(badge)
            self.badge_repository.commit()

        except:
            self.badge_repository.rollback()
            raise

        return BadgeCreateResponse()

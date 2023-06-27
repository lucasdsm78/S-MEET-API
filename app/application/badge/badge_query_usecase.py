from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel
from fastapi.responses import FileResponse

from app.application.badge.badge_query_model import BadgeReadModel, UserBadgeReadModel
from app.application.user.user_query_model import UserReadModel, ListParticipantsResponse
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.user.exception.user_exception import UserNotFoundError


class BadgeQueryUseCase(ABC):

    @abstractmethod
    def fetch_badges(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_user_badges(self) -> dict:
        raise NotImplementedError


    @abstractmethod
    def fetch_badges_by_user_id(self, user_id: int) -> dict:
        raise NotImplementedError


class BadgeQueryUseCaseImpl(BadgeQueryUseCase, BaseModel):
    badge_repository: BadgeRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_badges(self) -> dict:
        try:
            badges = self.badge_repository.find_badges()
            return dict(
                badges=list(map(lambda badge: BadgeReadModel.from_entity(
                    badge=badge), badges))
            )

        except Exception as e:
            raise


    def fetch_user_badges(self) -> dict:
        try:
            user_badges = self.badge_repository.find_user_badges()
            return dict(
                user_badges=list(map(lambda user_badge: UserBadgeReadModel.from_entity(
                    user_badge=user_badge), user_badges))
            )

        except Exception as e:
            raise

    def fetch_badges_by_user_id(self, user_id: int) -> dict:
        try:
            badges = self.badge_repository.find_badges_by_user_id(user_id)

            return dict(
                badges=list(map(lambda badge: UserBadgeReadModel.from_entity(
                    user_badge=badge), badges))
            )
        except Exception as e:
            raise
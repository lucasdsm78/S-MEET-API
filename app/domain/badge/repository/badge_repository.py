from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.activity.model.activity import Activity
from app.domain.badge.model.badge import Badge
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge


class BadgeRepository(ABC):
    """BadgeRepository defines a repository interface for Badge entity."""

    @abstractmethod
    def create(self, badge: Badge) -> Optional[Badge]:
        raise NotImplementedError

    @abstractmethod
    def find_badges(self) -> List[Badge]:
        raise NotImplementedError

    @abstractmethod
    def find_user_badges(self) -> List[UserBadge]:
        raise NotImplementedError

    @abstractmethod
    def find_user_badges_by_user_id(self, user_id: int) -> List[UserBadge]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, badge_id: int) -> Optional[Badge]:
        raise NotImplementedError

    @abstractmethod
    def find_user_badge_by_user_id_badge_id(self, user_id: int, badge_id: int) -> Optional[UserBadge]:
        raise NotImplementedError

    @abstractmethod
    def find_user_badge(self, badge_id: int, user_id: int) -> bool:
        raise NotImplementedError
    
    @abstractmethod
    def find_by_name(self, name: str) -> Optional[Badge]:
        raise NotImplementedError

    @abstractmethod
    def find_badges_by_user_id(self, user_id: int) -> List[Badge]:
        raise NotImplementedError

    @abstractmethod
    def add_badge_to_user(self, user_badge: UserBadge) -> Optional[UserBadge]:
        raise NotImplementedError

    @abstractmethod
    def update_user_badge(self, user_badge: UserBadge):
        raise NotImplementedError

    @abstractmethod
    def delete_user_badge(self, user_badge_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
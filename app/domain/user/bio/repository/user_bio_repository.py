from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user.model.user_bio import UserBio


class UserBioRepository(ABC):
    """UserBioRepository defines a repository interface for UserBio entity."""

    @abstractmethod
    def create(self, user_bio: UserBio) -> int:
        raise NotImplementedError

    @abstractmethod
    def update(self, user_bio: UserBio) -> Optional[UserBio]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def find_bio_by_user_id(self, user_id) -> Optional[UserBio]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, user_bio_id) -> Optional[UserBio]:
        raise NotImplementedError

    @abstractmethod
    def last(self) -> int:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

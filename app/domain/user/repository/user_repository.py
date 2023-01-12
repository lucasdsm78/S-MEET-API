from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user.model.user import User


class UserRepository(ABC):
    """UserRepository defines a repository interface for User entity."""

    @abstractmethod
    def create(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_email(self, email: str) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

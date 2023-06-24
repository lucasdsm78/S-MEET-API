from abc import ABC, abstractmethod
from typing import Optional, List

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
    def find_by_id(self, user_id: int) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def find_users(self) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def find_users_by_activity(self, activity_id: int) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def update_user(self, user: User) -> Optional[User]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional

from app.domain.user.model.school import School


class SchoolRepository(ABC):
    """SchoolRepository defines a repository interface for User entity."""

    @abstractmethod
    def create(self, school: School) -> Optional[School]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def find_by_name(self, name: str) -> Optional[School]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

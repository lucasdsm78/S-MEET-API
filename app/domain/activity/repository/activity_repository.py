from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.activity.model.activity import Activity


class ActivityRepository(ABC):
    """ActivityRepository defines a repository interface for Activity entity."""

    @abstractmethod
    def create(self, activity: Activity) -> Optional[Activity]:
        raise NotImplementedError

    @abstractmethod
    def find_activities(self) -> List[Activity]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

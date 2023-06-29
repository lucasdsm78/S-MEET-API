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
    def find_events(self) -> List[Activity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, activity_id: int) -> Optional[Activity]:
        raise NotImplementedError

    @abstractmethod
    def find_by_uuid(self, activity_uuid: str) -> Optional[Activity]:
        raise NotImplementedError

    @abstractmethod
    def delete_activity(self, activity_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

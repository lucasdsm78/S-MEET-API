from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.activity.model.activity_participants import ActivityParticipant


class ActivityParticipantRepository(ABC):
    """ActivityParticipantRepository defines a repository interface for ActivityParticipant entity."""

    @abstractmethod
    def add_participant(self, activity_participant: ActivityParticipant) -> Optional[ActivityParticipant]:
        raise NotImplementedError

    @abstractmethod
    def get_participation(self, activity_id: int, user_id: int) -> Optional[ActivityParticipant]:
        raise NotImplementedError

    @abstractmethod
    def find_participation(self, activity_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def find_participants_by_activity_id(self, activity_id: int) -> List[ActivityParticipant]:
        raise NotImplementedError

    @abstractmethod
    def count_participations(self, activity_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def delete_participant(self, activity_participant_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
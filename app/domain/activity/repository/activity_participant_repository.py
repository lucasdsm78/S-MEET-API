from abc import ABC, abstractmethod
from typing import Optional

from app.domain.activity.model.activity_participants import ActivityParticipant


class ActivityParticipantRepository(ABC):
    """ActivityParticipantRepository defines a repository interface for ActivityParticipant entity."""

    @abstractmethod
    def add_participant(self, activity_participant: ActivityParticipant) -> Optional[ActivityParticipant]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
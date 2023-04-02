from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat.room.model.room_participant import RoomParticipant


class RoomParticipantRepository(ABC):
    """RoomParticipantRepository defines a repository interface for RoomParticipantRepository entity."""

    @abstractmethod
    def add_participant(self, room_participant: RoomParticipant) -> Optional[RoomParticipant]:
        raise NotImplementedError

    @abstractmethod
    def find_conversations_by_user(self, user_id: int) -> List[RoomParticipant]:
        raise NotImplementedError

    @abstractmethod
    def find_participants_by_room(self, room_id: int) -> List[RoomParticipant]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

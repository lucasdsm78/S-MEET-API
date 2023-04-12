from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat.room.model.room import Room
from app.domain.chat.room.model.room_participant import RoomParticipant
from app.domain.user.model.user import User


class RoomParticipantRepository(ABC):
    """RoomParticipantRepository defines a repository interface for RoomParticipantRepository entity."""

    @abstractmethod
    def add_participant(self, room_participant: RoomParticipant):
        raise NotImplementedError

    @abstractmethod
    def delete_participant_room(self, room_participant_id: int):
        raise NotImplementedError

    @abstractmethod
    def find_conversations_by_user(self, user_id: int) -> List[Room]:
        raise NotImplementedError

    @abstractmethod
    def find_participants_by_room(self, room_id: int) -> List[User]:
        raise NotImplementedError

    @abstractmethod
    def get_participation_room(self, room_id: int, user_id: int) -> Optional[RoomParticipant]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat.room.model.room import Room


class RoomRepository(ABC):
    """RoomRepository defines a repository interface for RoomRepository entity."""

    @abstractmethod
    def create(self, room: Room) -> Optional[Room]:
        raise NotImplementedError

    @abstractmethod
    def find_room_by_id(self, room_id: int) -> Optional[Room]:
        raise NotImplementedError

    def find_by_uuid(self, room_uuid: str) -> Optional[Room]:
        raise NotImplementedError

    @abstractmethod
    def delete_room(self, room_id: int):
        raise NotImplementedError

    @abstractmethod
    def update_room(self, room: Room) -> Optional[Room]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

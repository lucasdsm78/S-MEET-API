from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat.message.model.message import Message


class MessageRepository(ABC):
    """MessageRepository defines a repository interface for Message entity."""

    @abstractmethod
    def create(self, message: Message) -> Optional[Message]:
        raise NotImplementedError

    @abstractmethod
    def find_messages_by_room(self, room_id: int) -> List[Message]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

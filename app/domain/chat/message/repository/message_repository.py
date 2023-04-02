from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.chat.message.model.message import Message


class ActivityRepository(ABC):
    """ActivityRepository defines a repository interface for Activity entity."""

    @abstractmethod
    def create(self, message: Message) -> Optional[Message]:
        raise NotImplementedError

    @abstractmethod
    def find_messages_by_chat(self, chat_id: int) -> List[Message]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

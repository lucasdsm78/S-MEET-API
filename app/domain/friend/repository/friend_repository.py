from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.friend.model.friend import Friend


class FriendRepository(ABC):
    """FriendRepository defines a repository interface for Friend entity."""

    @abstractmethod
    def add(self, friend: Friend) -> Optional[Friend]:
        raise NotImplementedError

    @abstractmethod
    def remove(self, friend: Friend):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def find_friend(self, friend_id: int) -> Optional[Friend]:
        raise NotImplementedError

    @abstractmethod
    def find_friends(self) -> List[Friend]:
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

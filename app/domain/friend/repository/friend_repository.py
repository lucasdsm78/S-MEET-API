from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.friend.model.friend import Friend


class FriendRepository(ABC):
    """FriendRepository defines a repository interface for Friend entity."""

    @abstractmethod
    def add(self, friend: Friend) -> Optional[Friend]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def find_friend(self, owner_profile_id: int, second_user_id: int) -> Optional[Friend]:
        raise NotImplementedError

    @abstractmethod
    def find_friends(self, user_id: int) -> List[Friend]:
        raise NotImplementedError

    @abstractmethod
    def get_status_friend(self, user_owner_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def check_friend(self, owner_profile_id: int, second_user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_friend(self, friend_id: int):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError

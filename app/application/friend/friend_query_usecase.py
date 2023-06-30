from abc import ABC, abstractmethod
from typing import Optional, List

from pydantic import BaseModel

from app.application.friend.friend_query_model import FriendReadModel
from app.domain.friend.repository.friend_repository import FriendRepository
from app.domain.friend.exception.friend_exception import FriendNotFoundError


class FriendQueryUseCase(ABC):

    @abstractmethod
    def get_friend(self, friend_id: int) -> Optional[FriendReadModel]:
        raise NotImplementedError
    
    @abstractmethod
    def get_friends(self) -> List[FriendReadModel]:
        raise NotImplementedError


class FriendQueryUseCaseImpl(FriendQueryUseCase, BaseModel):
    friend_repository: FriendRepository

    class Config:
        arbitrary_types_allowed = True

    def get_friend(self, friend_id: int) -> Optional[FriendReadModel]:
        try:
            friend = self.friend_repository.find_friend(friend_id)
            if friend is None:
                raise FriendNotFoundError

        except Exception as e:
            raise

        return FriendReadModel.from_entity(friend)

    def get_friends(self) -> dict:
        try:
            friends = self.friend_repository.find_friends()
            return dict(
                friends=list(map(lambda friend: FriendReadModel.from_entity(
                    friend=friend), friends))
            )

        except Exception as e:
            raise

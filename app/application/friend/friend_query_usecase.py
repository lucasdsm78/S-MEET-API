from abc import ABC, abstractmethod
from typing import Optional, List

from pydantic import BaseModel

from app.application.friend.friend_query_model import FriendReadModel
from app.domain.friend.repository.friend_repository import FriendRepository
from app.domain.friend.exception.friend_exception import FriendNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError
from app.domain.user.repository.user_repository import UserRepository


class FriendQueryUseCase(ABC):

    @abstractmethod
    def get_friends(self, user_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_status(self, current_user_id: int, id_second_user: int) -> bool:
        raise NotImplementedError


class FriendQueryUseCaseImpl(FriendQueryUseCase, BaseModel):
    friend_repository: FriendRepository
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True

    def get_friends(self, user_id: int) -> dict:
        try:
            users = []
            friends = self.friend_repository.find_friends(user_id)
            for friend in friends:
                user = self.user_repository.find_by_id(friend.id_second_user)
                users.append(user)

            return dict(
                friends=list(map(lambda user: FriendReadModel.from_entity(
                    user=user), users))
            )

        except Exception as e:
            raise

    def get_status(self, current_user_id: int, id_second_user: int) -> bool:
        try:
            user_second = self.user_repository.find_by_id(id_second_user)
            current_user = self.user_repository.find_by_id(current_user_id)

            if user_second is None:
                raise UserNotFoundError
            if current_user is None:
                raise UserNotFoundError

            status = self.friend_repository.check_friend(current_user.id, user_second.id)

            return status

        except Exception as e:
            raise

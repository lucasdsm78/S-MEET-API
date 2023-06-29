from abc import ABC, abstractmethod

from app.application.friend.friend_command_model import FriendAddModel, FriendAddResponse, FriendRemoveResponse
from app.domain.services.hash import Hash
from app.domain.services.manager_token import ManagerToken
from app.domain.friend.exception.friend_exception import FriendNotFoundError, FriendAlreadyExistsError

from app.domain.friend.model.friend import Friend
from app.domain.friend.repository.friend_repository import FriendRepository
from app.domain.user.repository.user_repository import UserRepository


class FriendCommandUseCase(ABC):
    """FriendCommandUseCase defines a command usecase inteface related Friend entity."""

    @abstractmethod
    def add(self, friend_id: int) -> FriendAddResponse:
        raise NotImplementedError

    @abstractmethod
    def remove(self, friend_id: int) -> FriendRemoveResponse:
        raise NotImplementedError


class FriendCommandUseCaseImpl(FriendCommandUseCase):
    """FriendCommandUseCaseImpl implements a command usecases related Friend entity."""

    def __init__(
            self,
            friend_repository: FriendRepository,
            user_repository: UserRepository
    ):
        self.friend_repository: FriendRepository = friend_repository
        self.user_repository: UserRepository = user_repository

    def create(self, data: int) -> FriendAddResponse:
        try:
            friend = Friend(
                id_owner_profile=self.user_repository.id,
                id_second_user=data
            )

            existing_friend = self.friend_repository.find_friend(friend.id)
            if existing_friend is not None:
                raise FriendAlreadyExistsError

            self.friend_repository.add(friend)
            self.friend_repository.commit()

            friend = self.friend_repository.find_friend(friend.id)
            if not friend:
                raise FriendNotFoundError(friend)

        except:
            self.friend_repository.rollback()
            raise

        return FriendAddResponse()

    def remove(self, data: Friend) -> FriendRemoveResponse:
        try:
            not_found_friend = self.friend_repository.find_friend(data.id)
            if not_found_friend is not None:
                raise FriendNotFoundError

            self.friend_repository.remove(data)
            self.friend_repository.commit()

            friend = self.friend_repository.find_friend(data.id)
            if not friend:
                raise FriendNotFoundError(friend)

        except:
            self.friend_repository.rollback()
            raise

        return FriendRemoveResponse()

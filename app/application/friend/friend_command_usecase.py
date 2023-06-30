from abc import ABC, abstractmethod

from app.application.friend.friend_command_model import FriendAddModel, FriendAddResponse, FriendRemoveResponse, \
    FriendUpdateResponse
from app.domain.friend.exception.friend_exception import FriendNotFoundError, FriendAlreadyExistsError, NotFriendError

from app.domain.friend.model.friend import Friend
from app.domain.friend.repository.friend_repository import FriendRepository
from app.domain.user.repository.user_repository import UserRepository


class FriendCommandUseCase(ABC):
    """FriendCommandUseCase defines a command usecase inteface related Friend entity."""

    @abstractmethod
    def add(self, owner_profile_id: int, second_user_id: int) -> FriendAddResponse:
        raise NotImplementedError

    @abstractmethod
    def remove(self, current_user_id: int, friend_id: int) -> FriendRemoveResponse:
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

    def add(self, owner_profile_id: int, second_user_id: int) -> FriendAddResponse:
        try:
            owner_profile = self.user_repository.find_by_id(owner_profile_id)
            second_user = self.user_repository.find_by_id(second_user_id)

            check_friend = self.friend_repository.check_friend(owner_profile.id, second_user.id)

            if check_friend is not False:
                raise FriendAlreadyExistsError

            friend = Friend(
                id_owner_profile=owner_profile.id,
                id_second_user=second_user.id,
                is_friend=False
            )

            self.friend_repository.add(friend)
            self.friend_repository.commit()

        except:
            self.friend_repository.rollback()
            raise

        return FriendAddResponse()

    def remove(self, current_user_id: int, friend_id: int) -> FriendRemoveResponse:
        try:
            existing_friend = self.friend_repository.find_friend(current_user_id, friend_id)
            if existing_friend is None:
                raise FriendNotFoundError

            self.friend_repository.delete_friend(existing_friend.id)
            self.friend_repository.commit()

        except:
            self.friend_repository.rollback()
            raise

        return FriendRemoveResponse()

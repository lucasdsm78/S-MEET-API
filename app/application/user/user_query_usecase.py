from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel
from fastapi.responses import FileResponse

from app.application.user.user_query_model import UserReadModel, ListParticipantsResponse
from app.domain.user.exception.user_exception import UserNotFoundError
from app.domain.user.repository.user_repository import UserRepository


class UserQueryUseCase(ABC):

    @abstractmethod
    def fetch_users(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_user_by_id(self, user_id: int) -> Optional[UserReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_users_by_activity(self, activity_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_image_user(self, user_id: int) -> FileResponse:
        raise NotImplementedError


class UserQueryUseCaseImpl(UserQueryUseCase, BaseModel):
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_users(self) -> dict:
        try:
            users = self.user_repository.find_users()
            return dict(
                users=list(map(lambda user: UserReadModel.from_entity(
                    user=user), users))
            )

        except Exception as e:
            raise

    def fetch_user_by_id(self, user_id: int) -> Optional[UserReadModel]:
        try:
            user = self.user_repository.find_by_id(user_id)
            if user is None:
                raise UserNotFoundError
        except:
            raise

        return UserReadModel.from_entity(user)

    def fetch_users_by_activity(self, activity_id: int) -> dict:
        try:
            users = self.user_repository.find_users_by_activity(activity_id)

            return dict(
                users=list(map(lambda user: ListParticipantsResponse.from_entity(
                    user=user), users))
            )
        except Exception as e:
            raise

    def get_image_user(self, user_id: int) -> FileResponse:
        user = self.user_repository.find_by_id(user_id)
        if not user:
            raise UserNotFoundError

        return FileResponse(user.image_profil)
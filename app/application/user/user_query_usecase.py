from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.application.user.user_query_model import UserReadModel
from app.domain.user.repository.user_repository import UserRepository


class UserQueryUseCase(ABC):

    @abstractmethod
    def fetch_users(self) -> dict:
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


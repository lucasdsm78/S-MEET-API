from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.user.bio.user_bio_query_model import UserBioReadModel
from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.exception.user_exception import UserBioNotFoundError


class UserBioQueryUseCase(ABC):

    @abstractmethod
    def fetch_user_bio_by_user_id(self, user_id: int) -> Optional[UserBioReadModel]:
        raise NotImplementedError


class UserBioQueryUseCaseImpl(UserBioQueryUseCase, BaseModel):
    user_bio_repository: UserBioRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_user_bio_by_user_id(self, user_id: int) -> Optional[UserBioReadModel]:
        try:
            user_bio = self.user_bio_repository.find_bio_by_user_id(user_id)
            if user_bio is None:
                raise UserBioNotFoundError
        except:
            raise

        return UserBioReadModel.from_entity(user_bio)
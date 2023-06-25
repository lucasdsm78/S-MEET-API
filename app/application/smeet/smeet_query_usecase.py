from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.application.smeet.smeet_query_model import SmeetReadModel
from app.domain.smeet.repository.smeet_repository import SmeetRepository
from app.domain.user.exception.user_exception import UserNotFoundError
from app.domain.user.repository.user_repository import UserRepository


class SmeetQueryUseCase(ABC):

    @abstractmethod
    def fetch_smeets(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_smeets_receive(self, user_receiver_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_smeets_sent(self, user_sender_id: int) -> dict:
        raise NotImplementedError


class SmeetQueryUseCaseImpl(SmeetQueryUseCase, BaseModel):
    smeet_repository: SmeetRepository
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True


    def fetch_smeets(self) -> dict:
        try:
            smeets = self.smeet_repository.find_smeets()
            return dict(
                smeets=list(map(lambda smeet: SmeetReadModel.from_entity(
                    smeet=smeet), smeets))
            )

        except Exception as e:
            raise

    def fetch_smeets_receive(self, user_receiver_id: int) -> dict:
        try:
            user_receiver = self.user_repository.find_by_id(user_receiver_id)
            if user_receiver is None:
                raise UserNotFoundError

            smeets = self.smeet_repository.find_smeets_by_user_receiver_id(user_receiver.id)
            return dict(
                smeets=list(map(lambda smeet: SmeetReadModel.from_entity(
                    smeet=smeet), smeets))
            )

        except Exception as e:
            raise

    def fetch_smeets_sent(self, user_sender_id: int) -> dict:
        try:
            user_sender = self.user_repository.find_by_id(user_sender_id)
            if user_sender is None:
                raise UserNotFoundError

            smeets = self.smeet_repository.find_smeets_by_user_sender_id(user_sender.id)
            return dict(
                smeets=list(map(lambda smeet: SmeetReadModel.from_entity(
                    smeet=smeet), smeets))
            )

        except Exception as e:
            raise
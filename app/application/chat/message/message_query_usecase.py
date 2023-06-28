from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.application.chat.message.message_query_model import MessageReadModel
from app.domain.chat.message.exception.message_exception import MessageNotFoundError
from app.domain.chat.message.model.message import Message
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.domain.chat.room.repository.room_repository import RoomRepository


class MessageQueryUseCase(ABC):

    @abstractmethod
    def find_messages_by_room(self, room_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def find_last_message_by_room_id(self, room_id: int) -> Message:
        raise NotImplementedError


class MessageQueryUseCaseImpl(MessageQueryUseCase, BaseModel):
    room_repository: RoomRepository
    message_repository: MessageRepository

    class Config:
        arbitrary_types_allowed = True

    def find_messages_by_room(self, room_id: int) -> dict:
        try:
            messages = self.message_repository.find_messages_by_room(room_id)

            return dict(
                messages=list(map(lambda message: MessageReadModel.from_entity(
                    message=message), messages))
            )
        except Exception as e:
            raise

    def find_last_message_by_room_id(self, room_id: int) -> Message:
        try:
            message = self.message_repository.last(room_id)
            if message is None:
                raise MessageNotFoundError
        except:
            raise

        return message
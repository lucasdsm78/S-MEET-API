from abc import ABC, abstractmethod
from typing import Optional, List

from pydantic import BaseModel

from app.application.chat.message.message_query_model import MessageReadModel
from app.application.chat.room.room_query_model import RoomReadModel, \
    ListConversationResponse, ListParticipationsRoomResponse
from app.domain.chat.message.model.message import Message
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.domain.chat.room.repository.room_repository import RoomRepository


class MessageQueryUseCase(ABC):

    @abstractmethod
    def find_messages_by_room(self, room_id: int) -> dict:
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
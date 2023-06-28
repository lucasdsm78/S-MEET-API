from abc import ABC, abstractmethod
from app.application.chat.message.message_command_model import MessageCreateModel, MessageCreateResponse
from app.domain.chat.message.model.message import Message
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.user.repository.user_repository import UserRepository


class MessageCommandUseCase(ABC):
    """MessageCommandUseCase defines a command usecase inteface related Message entity."""

    @abstractmethod
    def create(self, data: MessageCreateModel, user_id: int):
        raise NotImplementedError


class MessageCommandUseCaseImpl(MessageCommandUseCase):
    """MessageCommandUseCaseImpl implements a command usecases related Message entity."""

    def __init__(
            self,
            message_repository: MessageRepository,
            user_repository: UserRepository,
            room_repository: RoomRepository
    ):
        self.message_repository: MessageRepository = message_repository
        self.user_repository: UserRepository = user_repository
        self.room_repository: RoomRepository = room_repository

    def create(self, data: MessageCreateModel, user_id: int):
        try:
            user = self.user_repository.find_by_id(user_id)
            room = self.room_repository.find_room_by_id(room_id=data.room_id)

            message = Message(
                content=data.content,
                room_id=room.id,
                user_id=user.id
            )

            self.message_repository.create(message)
            self.message_repository.commit()
        except:
            self.message_repository.rollback()
            raise

        return MessageCreateResponse()
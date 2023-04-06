from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.chat.room.room_query_model import RoomReadModel, \
    ListConversationResponse, ListParticipationsRoomResponse
from app.domain.chat.room.exception.room_exception import RoomNotFoundError
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository


class RoomQueryUseCase(ABC):

    @abstractmethod
    def find_room_by_id(self, room_id: int) -> Optional[RoomReadModel]:
        raise NotImplementedError

    @abstractmethod
    def fetch_conversations_by_user(self, user_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_participations_by_room(self, room_id: int) -> dict:
        raise NotImplementedError


class RoomQueryUseCaseImpl(RoomQueryUseCase, BaseModel):
    room_repository: RoomRepository
    room_participant_repository: RoomParticipantRepository

    class Config:
        arbitrary_types_allowed = True

    def find_room_by_id(self, room_id: int) -> Optional[RoomReadModel]:
        try:
            room = self.room_repository.find_room_by_id(room_id)
            if room is None:
                raise RoomNotFoundError
        except:
            raise

        return RoomReadModel.from_entity(room)

    def fetch_conversations_by_user(self, user_id: int) -> dict:
        try:
            conversations = self.room_participant_repository.find_conversations_by_user(user_id)

            return dict(
                conversations=list(map(lambda room: ListConversationResponse.from_entity(
                    room=room), conversations))
            )
        except Exception as e:
            raise

    def fetch_participations_by_room(self, room_id: int) -> dict:
        try:
            participations = self.room_participant_repository.find_participants_by_room(room_id)

            return dict(
                participations=list(map(lambda user: ListParticipationsRoomResponse.from_entity(
                    user=user), participations))
            )
        except Exception as e:
            raise
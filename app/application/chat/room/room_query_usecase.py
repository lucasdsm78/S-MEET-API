from abc import ABC, abstractmethod
from typing import Optional
import shortuuid

from pydantic import BaseModel

from app.application.chat.room.room_query_model import RoomReadModel, \
    ListConversationResponse, ListParticipationsRoomResponse
from app.domain.chat.room.exception.room_exception import RoomNotFoundError
from app.domain.chat.room.model.room import Room
from app.domain.chat.room.model.room_participant import RoomParticipant
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.user.repository.user_repository import UserRepository


class RoomQueryUseCase(ABC):

    @abstractmethod
    def find_room_by_id(self, room_id: int) -> Room:
        raise NotImplementedError

    @abstractmethod
    def fetch_conversations_by_user(self, user_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_participations_by_room(self, room_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def find_room_by_user_connected_user_id(self, user_connected_id: int, user_id: int) -> int:
        raise NotImplementedError


class RoomQueryUseCaseImpl(RoomQueryUseCase, BaseModel):
    room_repository: RoomRepository
    room_participant_repository: RoomParticipantRepository
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True

    def find_room_by_id(self, room_id: int) -> Room:
        try:
            room = self.room_repository.find_room_by_id(room_id)
            if room is None:
                raise RoomNotFoundError
        except:
            raise

        return room

    def find_room_by_user_connected_user_id(self, user_connected_id: int, user_id: int) -> int:
        try:
            user_connected = self.user_repository.find_by_id(user_connected_id)
            user = self.user_repository.find_by_id(user_id)
            rooms = self.room_participant_repository.find_room_by_user_connected_user_id(user_connected_id, user_id)
            print(len(rooms))
            if len(rooms) != 2:
                try:
                    # create room
                    uuid = shortuuid.uuid()
                    room = Room(
                        name=f"Room {user_connected.pseudo} and {user.pseudo}",
                        uuid=uuid,
                        description=f"Room between {user_connected.pseudo} and {user.pseudo}",
                        school_id=user_connected.school.id,
                        image_room=""
                    )

                    self.room_repository.create(room)
                    self.room_repository.commit()

                    existing_room = self.room_repository.find_by_uuid(uuid)

                    room_id = existing_room.id

                    # add participant
                    room_participant_user_connected = RoomParticipant(
                        user_id=user_connected.id,
                        room_id=existing_room.id
                    )

                    room_participant_user_id = RoomParticipant(
                        user_id=user.id,
                        room_id=existing_room.id
                    )

                    self.room_participant_repository.add_participant(room_participant_user_connected)
                    self.room_participant_repository.add_participant(room_participant_user_id)
                    self.room_participant_repository.commit()

                except:
                    self.room_repository.rollback()
                    self.room_participant_repository.rollback()
                    raise

            else:
                existing_room = self.room_repository.find_room_by_id(rooms[0].room_id)
                room_id = existing_room.id
        except:
            raise

        return room_id

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
            print(e)
            raise
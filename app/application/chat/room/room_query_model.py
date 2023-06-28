from typing import Optional

from pydantic import Field, BaseModel

from app.domain.chat.room.model.room import Room
from app.domain.user.model.user import User


class RoomReadModel(BaseModel):
    """RoomReadModel represents data structure as a read model."""

    id: int
    name: str
    uuid: str
    school_id: int
    users: list
    messages: list

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(room: Room) -> "RoomReadModel":
        return RoomReadModel(
            id=room.id,
            uuid=room.uuid,
            name=room.name,
            school_id=room.school_id,
            users=room.users,
            messages=room.messages
        )


class ListConversationResponse(BaseModel):
    room_id: int
    name: str
    description: str
    image_room: str

    @staticmethod
    def from_entity(room: Room) -> "ListConversationResponse":
        return ListConversationResponse(
            room_id=room.id,
            name=room.name,
            description=room.description,
            image_room=room.image_room
        )


class ListParticipationsRoomResponse(BaseModel):
    id: int
    email: str
    first_name: str
    last_name: str
    uuid: str
    image_profil: str
    pseudo: str
    createdAt: int
    updatedAt: int
    user_bio_id: int

    @staticmethod
    def from_entity(user: User) -> "ListParticipationsRoomResponse":
        return ListParticipationsRoomResponse(
            id=user.id,
            uuid=user.uuid,
            image_profil=user.image_profil,
            email=user.email.value,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
            first_name=user.first_name,
            last_name=user.last_name,
            pseudo=user.pseudo,
            user_bio_id=user.user_bio_id
        )

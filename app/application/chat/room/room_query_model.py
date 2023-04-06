from typing import Optional

from pydantic import Field, BaseModel

from app.domain.chat.room.model.room import Room
from app.domain.user.model.user import User


class RoomReadModel(BaseModel):
    """RoomReadModel represents data structure as a read model."""

    id: int
    name: str
    school_id: int
    users: list
    messages: list

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(room: Room) -> "RoomReadModel":
        return RoomReadModel(
            id=room.id,
            name=room.name,
            school_id=room.school_id,
            users=room.users,
            messages=room.messages
        )


class ListConversationResponse(BaseModel):
    name: str
    description: str
    image_room: str

    @staticmethod
    def from_entity(room: Room) -> "ListConversationResponse":
        return ListConversationResponse(
            name=room.name,
            description=room.description,
            image_room=room.image_room
        )


class ListParticipationsRoomResponse(BaseModel):
    pseudo: str
    first_name: str
    last_name: str

    @staticmethod
    def from_entity(user: User) -> "ListParticipationsRoomResponse":
        return ListParticipationsRoomResponse(
            pseudo=user.pseudo,
            first_name=user.first_name,
            last_name=user.last_name
        )

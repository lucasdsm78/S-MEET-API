from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.domain.chat.message.model.message import Message
from app.domain.chat.room.model.room import Room
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBRoom(Base):
    """DBRoom is a data transfer object associated with Room entity."""

    __tablename__ = "room"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    name: Union[str, Column] = Column(String, nullable=False)
    description: Union[str, Column] = Column(String, nullable=False)
    image_room: Union[str, Column] = Column(String, nullable=False)
    school_id: Union[int, Column] = Column(Integer, ForeignKey('school.id'))
    school = relationship("DBSchool", back_populates='room')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    message = relationship("DBMessage", back_populates="room")
    room_participants = relationship("DBRoomParticipants", back_populates="room")

    def to_entity(self) -> Room:
        return Room(
            id=self.id,
            name=self.name,
            description=self.description,
            school_id=self.school_id,
            image_room=self.image_room,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_entity(room: Room, db_room: Optional["DBRoom"] = None) -> "DBRoom":
        now = unixtimestamp()
        room_db_to_update = db_room if db_room is not None else DBRoom()
        room_db_to_update.id = room.id
        room_db_to_update.name = room.name
        room_db_to_update.image_room = room.image_room
        room_db_to_update.description = room.description
        room_db_to_update.school_id = room.school_id
        room_db_to_update.created_at = now
        room_db_to_update.updated_at = now
        return room_db_to_update

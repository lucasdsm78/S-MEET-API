from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.chat.room.model.room_participant import RoomParticipant
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBRoomParticipants(Base):
    __tablename__ = "room_participants"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='room_participants')
    room_id: Union[int, Column] = Column(Integer, ForeignKey('room.id'))
    room = relationship("DBRoom", back_populates='room_participants')

    def to_entity(self) -> RoomParticipant:
        return RoomParticipant(
            id=self.id,
            user_id=self.user_id,
            room_id=self.room_id,
        )

    @staticmethod
    def from_entity(room_participant: RoomParticipant, db_room_participant:
    Optional["DBRoomParticipants"] = None) -> "DBRoomParticipants":
        room_participant_db_to_update = db_room_participant if db_room_participant \
                                                               is not None else DBRoomParticipants()
        room_participant_db_to_update.id = room_participant.id
        room_participant_db_to_update.user_id = room_participant.user_id
        room_participant_db_to_update.room_id = room_participant.room_id
        return room_participant_db_to_update

from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.domain.chat.message.model.message import Message
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBMessage(Base):
    """DBMessage is a data transfer object associated with Message entity."""

    __tablename__ = "message"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    content: Union[str, Column] = Column(String, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='messages')
    room_id: Union[int, Column] = Column(Integer, ForeignKey('room.id'))
    room = relationship("DBRoom", back_populates='message')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Message:
        return Message(
            id=self.id,
            content=self.content,
            room_id=self.room_id,
            user_id=self.user_id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_entity(message: Message, db_message: Optional["DBMessage"] = None) -> "DBMessage":
        now = unixtimestamp()
        message_db_to_update = db_message if db_message is not None else DBMessage()
        message_db_to_update.id = message.id
        message_db_to_update.content = message.content
        message_db_to_update.user_id = message.user_id
        message_db_to_update.room_id = message.room_id
        message_db_to_update.created_at = now
        message_db_to_update.updated_at = now
        return message_db_to_update

from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.smeet.model.smeet import Smeet
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBSmeet(Base):
    """DBSmeet is a data transfer object associated with Smeet entity."""

    __tablename__ = "smeet"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    content: Union[str, Column] = Column(String, nullable=False)
    is_edited: Union[bool, Column] = Column(Boolean, nullable=False)
    user_sender_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user_receiver_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    user_sender = relationship("DBUser", foreign_keys=[user_sender_id])
    user_receiver = relationship("DBUser", foreign_keys=[user_receiver_id])

    def to_entity(self) -> Smeet:
        return Smeet(
            id=self.id,
            content=self.content,
            user_sender=self.user_sender_id,
            user_receiver=self.user_receiver_id,
            is_edited=self.is_edited,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(smeet: Smeet, db_smeet: Optional["DBSmeet"] = None) -> "DBSmeet":
        now = unixtimestamp()
        smeet_db_to_update = db_smeet if db_smeet is not None else DBSmeet()
        smeet_db_to_update.id = smeet.id
        smeet_db_to_update.content = smeet.content
        smeet_db_to_update.user_sender_id = smeet.user_sender
        smeet_db_to_update.user_receiver_id = smeet.user_receiver
        smeet_db_to_update.is_edited = smeet.is_edited
        smeet_db_to_update.created_at = now
        return smeet_db_to_update
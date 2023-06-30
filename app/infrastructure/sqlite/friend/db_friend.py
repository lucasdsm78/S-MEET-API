from typing import Union, Optional
from datetime import datetime

from sqlalchemy import Column, Integer, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.friend.model.friend import Friend
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBFriend(Base):
    """DBFriend is a data transfer object associated with Friend entity."""

    __tablename__ = "friend"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    id_owner_profile: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    id_second_user: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    is_friend: Union[bool, Column] = Column(Boolean, nullable=False)
    owner_profile = relationship("DBUser", foreign_keys=[id_owner_profile])
    second_user = relationship("DBUser", foreign_keys=[id_second_user])
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Friend:
        return Friend(
            id=self.id,
            id_owner_profile=self.id_owner_profile,
            id_second_user=self.id_second_user,
            is_friend=self.is_friend,
            created_at=self.created_at
        )

    @staticmethod
    def from_entity(friend: Friend, db_friend: Optional["DBFriend"] = None) -> "DBFriend":
        now = unixtimestamp()
        friend_db_to_update = db_friend if db_friend is not None else DBFriend()
        friend_db_to_update.id = friend.id
        friend_db_to_update.id_owner_profile = friend.id_owner_profile
        friend_db_to_update.id_second_user = friend.id_second_user
        friend_db_to_update.is_friend = friend.is_friend
        friend_db_to_update.created_at = now
        return friend_db_to_update

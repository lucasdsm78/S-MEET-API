from typing import Union, Optional

from sqlalchemy import Column, Integer, ForeignKey

from app.domain.friend.model.friend import Friend
from app.infrastructure.sqlite.database import Base


class DBFriend(Base):
    """DBFriend is a data transfer object associated with Friend entity."""

    __tablename__ = "friend"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    id_owner_profile: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    id_second_user: Union[int, Column] = Column(Integer, ForeignKey('user.id'))

    def to_entity(self) -> Friend:
        return Friend(
            id=self.id,
            id_owner_profile=self.id_owner_profile,
            id_second_user=self.id_second_user
        )

    @staticmethod
    def from_entity(friend: Friend, db_friend: Optional["DBFriend"] = None) -> "DBFriend":
        friend_db_to_update = db_friend if db_friend is not None else DBFriend()
        friend_db_to_update.id = friend.id
        friend_db_to_update.id_owner_profile = friend.id_owner_profile
        friend_db_to_update.id_second_user = friend.id_second_user
        return friend_db_to_update

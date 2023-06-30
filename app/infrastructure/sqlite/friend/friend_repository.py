from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.friend.exception.friend_exception import FriendNotFoundError
from app.domain.friend.model.friend import Friend
from app.domain.friend.repository.friend_repository import FriendRepository
from app.infrastructure.sqlite.friend.db_friend import DBFriend


class FriendRepositoryImpl(FriendRepository):
    """FriendRepositoryImpl implements CRUD operations related Friend entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_friend(self, friend_id: int) -> Optional[Friend]:
        try:
            friend_db = self.session.query(DBFriend).filter_by(id=friend_id).one()
        except NoResultFound:
            raise FriendNotFoundError
        except Exception:
            raise

        return friend_db.to_entity()

    def add(self, friend: Friend):
        friend_db = DBFriend.from_entity(friend)
        try:
            self.session.add(friend_db)
        except:
            raise

    def remove(self, friend: Friend):
        friend_db = DBFriend.from_entity(friend)
        try:
            self.session.delete(friend_db)
        except:
            raise

    def find_friends(self) -> List[Friend]:
        try:
            friend_dbs = (
                self.session.query(DBFriend)
                .order_by(DBFriend.last_name)
                .all()
            )
        except:
            raise

        if len(friend_dbs) == 0:
            return []

        return list(map(lambda friend_db: friend_db.to_entity(), friend_dbs))

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

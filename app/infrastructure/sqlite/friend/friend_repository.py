from typing import Optional, List

from sqlalchemy import and_
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

    def find_friend(self, owner_profile_id: int, second_user_id: int) -> Optional[Friend]:
        try:
            friend_db = self.session.query(DBFriend).filter(
                    ((DBFriend.id_owner_profile == owner_profile_id) & (DBFriend.id_second_user == second_user_id)) |
                    ((DBFriend.id_owner_profile == second_user_id) & (DBFriend.id_second_user == owner_profile_id))
                ).one()

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

    def delete_friend(self, friend_id: int):
        try:
            self.session.query(DBFriend).filter_by(id=friend_id).delete()
        except:
            raise

    def find_friends(self, user_id: int) -> List[Friend]:
        try:
            friend_dbs = (
                self.session.query(DBFriend)
                .filter_by(is_friend=True)
                .filter((DBFriend.id_owner_profile == user_id) | (DBFriend.id_second_user == user_id))
                .all()
            )
        except:
            raise

        if len(friend_dbs) == 0:
            return []

        return list(map(lambda friend_db: friend_db.to_entity(), friend_dbs))

    def get_status_friend(self, user_owner_id: int, user_id: int) -> bool:
        try:
            friend_db = (self.session.query(DBFriend).filter_by(id_owner_profile = user_owner_id, id_second_user = user_id)).one()

        except Exception:
            raise

        return friend_db.is_friend


    def check_friend(self, owner_profile_id: int, second_user_id: int) -> bool:
        try:
            result = False
            friend_db = self.session.query(DBFriend).filter(
                    ((DBFriend.id_owner_profile == owner_profile_id) & (DBFriend.id_second_user == second_user_id)) |
                    ((DBFriend.id_owner_profile == second_user_id) & (DBFriend.id_second_user == owner_profile_id))
                ).count()

            if friend_db != 0:
                result = True
        except Exception:
            raise

        return result


    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

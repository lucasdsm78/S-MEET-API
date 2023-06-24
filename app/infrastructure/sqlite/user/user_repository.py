from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.user.exception.user_exception import UserNotFoundError
from app.domain.user.model.user import User
from app.domain.user.repository.user_repository import UserRepository
from app.infrastructure.sqlite.activity.db_activity_participants import DBActivityParticipants
from app.infrastructure.sqlite.user.db_user import DBUser


class UserRepositoryImpl(UserRepository):
    """UserRepositoryImpl implements CRUD operations related User entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_email(self, email: str) -> Optional[User]:
        try:
            user_db = self.session.query(DBUser).filter_by(email=email).one()
        except NoResultFound:
            return None
        except:
            raise

        return user_db.to_entity()

    def find_by_id(self, user_id: int) -> Optional[User]:
        try:
            user_db = self.session.query(DBUser).filter_by(id=user_id).one()
        except NoResultFound:
            raise UserNotFoundError
        except Exception:
            raise

        return user_db.to_entity()

    def create(self, user: User):
        user_db = DBUser.from_entity(user)
        try:
            self.session.add(user_db)
        except:
            raise

    def find_users(self) -> List[User]:
        try:
            user_dbs = (
                self.session.query(DBUser)
                .order_by(DBUser.last_name)
                .all()
            )
        except:
            raise

        if len(user_dbs) == 0:
            return []

        return list(map(lambda user_db: user_db.to_entity(), user_dbs))

    def find_users_by_activity(self, activity_id: int) -> List[User]:
        try:
            user_dbs = (
                self.session.query(DBUser)
                .join(DBActivityParticipants)
                .filter(DBActivityParticipants.activity_id == activity_id)
                .order_by(DBUser.last_name)
                .all()
            )
        except:
            raise

        if len(user_dbs) == 0:
            return []

        return list(map(lambda user_db: user_db.to_entity(), user_dbs))

    def delete_user(self, user_id: int):
        try:
            self.session.query(DBUser).filter_by(id=user_id).delete()
        except:
            raise

    def update_user(self, user: User):
        try:
            _user = self.session.query(DBUser).filter_by(id=user.id).one()
            user_db = DBUser.from_entity(user, _user)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

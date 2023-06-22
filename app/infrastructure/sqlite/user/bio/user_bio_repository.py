from typing import Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.exception.user_exception import UserBioNotFoundError
from app.domain.user.model.user_bio import UserBio
from app.infrastructure.sqlite.user.bio.db_user_bio import DBUserBio
from app.infrastructure.sqlite.user.db_user import DBUser


class UserBioRepositoryImpl(UserBioRepository):
    """UserBioRepositoryImpl implements CRUD operations related UserBio entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_bio_by_user_id(self, user_id) -> Optional[UserBio]:
        try:
            user_bio_db = self.session.query(DBUserBio) \
                .join(DBUser) \
                .filter(DBUser.user_bio_id == DBUserBio.id) \
                .filter_by(id=user_id) \
                .one()
        except NoResultFound:
            raise UserBioNotFoundError
        except Exception:
            raise

        return user_bio_db.to_entity()

    def find_by_id(self, user_bio_id: int) -> Optional[UserBio]:
        try:
            user_bio_db = self.session.query(DBUserBio).filter_by(id=user_bio_id).one()
        except NoResultFound:
            raise UserBioNotFoundError
        except Exception:
            raise

        return user_bio_db.to_entity()

    def last(self) -> int:
        try:
            last_user_bio_id = self.session.query(DBUserBio).order_by(DBUserBio.id.desc()).first()
        except NoResultFound:
            raise UserBioNotFoundError
        except Exception:
            raise

        return last_user_bio_id.id

    def create(self, user_bio: UserBio):
        print(user_bio.id)
        user_bio_db = DBUserBio.from_entity(user_bio)
        try:
            self.session.add(user_bio_db)
            return user_bio_db.id
        except:
            raise

    def update(self, user_bio: UserBio):
        try:
            _user_bio = self.session.query(DBUserBio).filter_by(id=user_bio.id).one()
            DBUserBio.from_entity(user_bio, _user_bio)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

from typing import List, Optional

from sqlalchemy import and_
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.badge.exception.badge_exception import BadgeNotFoundError, UserBadgeNotFoundError
from app.domain.badge.model.badge import Badge
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.infrastructure.sqlite.badge.db_badge import DBBadge
from app.infrastructure.sqlite.badge.db_user_badge import DBUserBadge


class BadgeRepositoryImpl(BadgeRepository):
    """BadgeRepositoryImpl implements CRUD operations related Badge entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, badge: Badge):
        badge_db = DBBadge.from_entity(badge)
        try:
            self.session.add(badge_db)
        except:
            raise

    def update_badge(self, badge: Badge):
        try:
            _badge = self.session.query(DBBadge).filter_by(id=badge.id).one()
            badge_db = DBBadge.from_entity(badge, _badge)
        except:
            raise

    def find_badges(self) -> List[Badge]:
        try:
            badge_dbs = (
                self.session.query(DBBadge)
                .order_by(DBBadge.name)
                .all()
            )
        except:
            raise

        if len(badge_dbs) == 0:
            return []

        return list(map(lambda badge_db: badge_db.to_entity(), badge_dbs))

    def find_user_badges(self) -> List[UserBadge]:
        try:
            user_badge_dbs = (
                self.session.query(DBUserBadge)
                .all()
            )
        except:
            raise

        if len(user_badge_dbs) == 0:
            return []

        return list(map(lambda user_badge_db: user_badge_db.to_entity(), user_badge_dbs))

    def find_user_badges_by_user_id(self, user_id: int) -> List[UserBadge]:
        try:
            user_badge_dbs = (
                self.session.query(DBUserBadge)
                .filter_by(user_id=user_id)
                .all()
            )
        except:
            raise

        if len(user_badge_dbs) == 0:
            return []

        return list(map(lambda user_badge_db: user_badge_db.to_entity(), user_badge_dbs))

    def find_by_id(self, badge_id: int) -> Optional[Badge]:
        try:
            badge_db = self.session.query(DBBadge).filter_by(id=badge_id).one()
        except NoResultFound:
            raise BadgeNotFoundError
        except Exception as e:
            raise

        return badge_db.to_entity()

    def find_user_badge_by_user_id_badge_id(self, user_id: int, badge_id: int) -> Optional[UserBadge]:
        try:
            user_badge_db = self.session.query(DBUserBadge).filter(and_(DBUserBadge.user_id == user_id, DBUserBadge.badge_id == badge_id)).one()
        except NoResultFound:
            raise UserBadgeNotFoundError
        except Exception as e:
            raise

        return user_badge_db.to_entity()

    def find_user_badge(self, badge_id: int, user_id: int) -> bool:
        try:
            result = False
            user_badge_db = self.session.query(DBUserBadge).filter_by(
                badge_id=badge_id,
                user_id=user_id
            ).count()

            if user_badge_db != 0:
                result = True
        except Exception:
            raise

        return result

    def find_by_name(self, name: str) -> Optional[Badge]:
        try:
            badge_db = self.session.query(DBBadge).filter_by(name=name).one()
        except NoResultFound:
            raise BadgeNotFoundError
        except Exception as e:
            raise

        return badge_db.to_entity()

    def find_badges_by_user_id(self, user_id: int) -> List[Badge]:
        try:
            badge_dbs = (
                self.session.query(DBUserBadge)
                .filter_by(user_id=user_id)
                .all()
            )
        except:
            raise

        print(badge_dbs)

        if len(badge_dbs) == 0:
            return []

        return list(map(lambda badge_db: badge_db.to_entity(), badge_dbs))

    def add_badge_to_user(self, user_badge: UserBadge):
        user_badge_db = DBUserBadge.from_entity(user_badge)
        try:
            self.session.add(user_badge_db)
        except:
            raise

    def update_user_badge(self, user_badge: UserBadge):
        try:
            _user_badge = self.session.query(DBUserBadge).filter_by(id=user_badge.id).one()
            user_badge_db = DBUserBadge.from_entity(user_badge, _user_badge)
        except:
            raise

    def delete_user_badge(self, user_badge_id: int):
        try:
            self.session.query(DBUserBadge).filter_by(id=user_badge_id).delete()
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
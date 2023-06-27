from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.stats.exception.stat_exception import StatNotFoundError
from app.domain.stats.model.stats import Stat
from app.domain.stats.repository.stat_repository import StatRepository
from app.domain.user.exception.user_exception import UserNotFoundError
from app.domain.user.model.user import User
from app.infrastructure.sqlite.activity.db_activity_participants import DBActivityParticipants
from app.infrastructure.sqlite.stats.db_stat import DBStat
from app.infrastructure.sqlite.user.db_user import DBUser


class StatRepositoryImpl(StatRepository):
    """StatRepositoryImpl implements CRUD operations related Stat entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_id(self, stat_id: int) -> Optional[Stat]:
        try:
            stat_db = self.session.query(DBStat).filter_by(id=stat_id).one()
        except NoResultFound:
            raise StatNotFoundError
        except Exception:
            raise

        return stat_db.to_entity()

    def find_by_user_id(self, user_id: int) -> Optional[Stat]:
        try:
            stat_db = self.session.query(DBStat).filter_by(user_id=user_id).one()
        except NoResultFound:
            raise StatNotFoundError
        except Exception:
            raise

        return stat_db.to_entity()

    def create(self, stat: Stat):
        stat_db = DBStat.from_entity(stat)
        try:
            self.session.add(stat_db)
        except:
            raise

    def delete_stat(self, stat_id: int):
        try:
            self.session.query(DBStat).filter_by(id=stat_id).delete()
        except:
            raise

    def update_stat(self, stat: Stat):
        try:
            _stat = self.session.query(DBStat).filter_by(id=stat.id).one()
            stat_db = DBStat.from_entity(stat, _stat)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.activity.exception.activity_exception import ActivityNotFoundError
from app.domain.activity.model.activity import Activity
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.infrastructure.sqlite.activity.db_activity import DBActivity


class ActivityRepositoryImpl(ActivityRepository):
    """ActivityRepositoryImpl implements CRUD operations related Activity entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, activity: Activity):
        activity_db = DBActivity.from_entity(activity)
        try:
            self.session.add(activity_db)
        except:
            raise

    def find_activities(self) -> List[Activity]:
        try:
            activity_dbs = (
                self.session.query(DBActivity)
                .filter_by(type='activity')
                .order_by(DBActivity.name)
                .all()
            )
        except:
            raise

        if len(activity_dbs) == 0:
            return []

        return list(map(lambda activity_db: activity_db.to_entity(), activity_dbs))

    def find_events(self) -> List[Activity]:
        try:
            activity_dbs = (
                self.session.query(DBActivity)
                .filter_by(type='event')
                .order_by(DBActivity.name)
                .all()
            )
        except:
            raise

        if len(activity_dbs) == 0:
            return []

        return list(map(lambda activity_db: activity_db.to_entity(), activity_dbs))

    def find_by_id(self, activity_id: int) -> Optional[Activity]:
        try:
            activity_db = self.session.query(DBActivity).filter_by(id=activity_id).one()
        except NoResultFound:
            raise ActivityNotFoundError
        except Exception as e:
            raise
        return activity_db.to_entity()

    def find_by_uuid(self, activity_uuid: str) -> Optional[Activity]:
        try:
            activity_db = self.session.query(DBActivity).filter_by(uuid=activity_uuid).one()
        except NoResultFound:
            raise ActivityNotFoundError
        except Exception as e:
            raise
        return activity_db.to_entity()

    def delete_activity(self, activity_id: int):
        try:
            self.session.query(DBActivity).filter_by(id=activity_id).delete()
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
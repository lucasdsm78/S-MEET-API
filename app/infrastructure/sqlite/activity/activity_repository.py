from typing import List

from sqlalchemy.orm.session import Session

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
                .order_by(DBActivity.name)
                .all()
            )
        except:
            raise

        if len(activity_dbs) == 0:
            return []

        return list(map(lambda activity_db: activity_db.to_entity(), activity_dbs))

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
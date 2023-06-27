from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session
from app.domain.notification.exception.notification_exception import NotificationNotFoundError
from app.domain.notification.model.notification import Notification
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.infrastructure.sqlite.notification.db_notification import DBNotification


class NotificationRepositoryImpl(NotificationRepository):
    """NotificationRepositoryImpl implements CRUD operations related Notification entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, notification: Notification):
        notification_db = DBNotification.from_entity(notification)
        try:
            self.session.add(notification_db)
        except:
            raise

    def find_notifications(self) -> List[Notification]:
        try:
            notification_dbs = (
                self.session.query(DBNotification)
                .order_by(DBNotification.created_at.desc())
                .all()
            )
        except:
            raise

        if len(notification_dbs) == 0:
            return []

        return list(map(lambda notification_db: notification_db.to_entity(), notification_dbs))

    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        try:
            notification_db = self.session.query(DBNotification).filter_by(id=notification_id).one()
        except NoResultFound:
            raise NotificationNotFoundError
        except Exception as e:
            raise

        return notification_db.to_entity()

    def find_notifications_by_user_id(self, user_id: int) -> List[Notification]:
        try:
            notification_dbs = (
                self.session.query(DBNotification)
                .filter_by(user_id=user_id)
                .all()
            )
        except:
            raise

        if len(notification_dbs) == 0:
            return []

        return list(map(lambda notification_db: notification_db.to_entity(), notification_dbs))

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
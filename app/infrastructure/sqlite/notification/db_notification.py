from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.notification.model.notification import Notification
from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.user.model.email import Email
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBNotification(Base):
    """DBNotification is a data transfer object associated with Notification entity."""

    __tablename__ = "notification"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    content: Union[str, Column] = Column(String, nullable=False)
    type_notification: Union[str, Column] = Column(String, nullable=False)
    is_read: Union[bool, Column] = Column(Boolean, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser")
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Notification:
        return Notification(
            id=self.id,
            content=self.content,
            type_notif=TypeNotification.from_str(self.type_notification),
            is_read=self.is_read,
            user=UserSummary(id=self.user_id, email=Email(self.user.email)),
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(notification: Notification, db_notification: Optional["DBNotification"] = None) -> "DBNotification":
        now = unixtimestamp()
        notification_db_to_update = db_notification if db_notification is not None else DBNotification()
        notification_db_to_update.id = notification.id
        notification_db_to_update.content = notification.content
        notification_db_to_update.type_notification = notification.type_notif.value
        notification_db_to_update.is_read = notification.is_read
        notification_db_to_update.user_id = notification.user.id
        notification_db_to_update.created_at = now
        return notification_db_to_update
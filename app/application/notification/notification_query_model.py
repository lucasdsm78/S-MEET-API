from typing import Optional

from pydantic import Field, BaseModel

from app.domain.activity.model.activity import Activity
from app.domain.notification.model.notification import Notification


class NotificationReadModel(BaseModel):
    """NotificationReadModel represents data structure as a read model."""

    id: int
    content: str
    type_notification: str
    is_read: bool
    user_id: int = Field(example=1)
    createdAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(notification: Notification) -> "NotificationReadModel":
        return NotificationReadModel(
            id=notification.id,
            type_notification=notification.type_notif.value,
            is_read=notification.is_read,
            content=notification.content,
            user_id=notification.user.id,
            createdAt=notification.created_at,
        )
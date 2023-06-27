from typing import Optional

from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.user.model.user_summary import UserSummary


class Notification:
    """Notification represents your collection of notification as an entity."""

    def __init__(
            self,
            content: str,
            is_read: bool,
            type_notif: TypeNotification,
            user: UserSummary,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.content: str = content
        self.is_read: bool = is_read
        self.type_notif: TypeNotification = type_notif
        self.user: UserSummary = user
        self.created_at: Optional[int] = created_at
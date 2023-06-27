from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.notification.model.notification import Notification


class NotificationRepository(ABC):
    """NotificationRepository defines a repository interface for Notification entity."""

    @abstractmethod
    def create(self, notification: Notification) -> Optional[Notification]:
        raise NotImplementedError

    @abstractmethod
    def find_notifications(self) -> List[Notification]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, notification_id: int) -> Optional[Notification]:
        raise NotImplementedError

    @abstractmethod
    def find_notifications_by_user_id(self, user_id: int) -> List[Notification]:
        raise NotImplementedError

    @abstractmethod
    def delete_notification(self, notification_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
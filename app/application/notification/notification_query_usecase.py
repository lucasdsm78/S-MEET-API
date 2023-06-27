from abc import ABC, abstractmethod

from pydantic import BaseModel

from app.application.notification.notification_query_model import NotificationReadModel
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.domain.user.repository.user_repository import UserRepository


class NotificationQueryUseCase(ABC):

    @abstractmethod
    def fetch_notifications(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_notifications_by_user_id(self, id: int) -> dict:
        raise NotImplementedError


class NotificationQueryUseCaseImpl(NotificationQueryUseCase, BaseModel):
    notification_repository: NotificationRepository
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_notifications(self) -> dict:
        try:
            notifications = self.notification_repository.find_notifications()
            return dict(
                notifications=list(map(lambda notification: NotificationReadModel.from_entity(
                    notification=notification), notifications))
            )

        except Exception as e:
            raise

    def fetch_notifications_by_user_id(self, id: int) -> dict:
        try:
            notifications = self.notification_repository.find_notifications_by_user_id(id)
            return dict(
                notifications=list(map(lambda notification: NotificationReadModel.from_entity(
                    notification=notification), notifications))
            )

        except Exception as e:
            raise
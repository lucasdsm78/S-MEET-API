from abc import ABC, abstractmethod
from app.application.notification.notification_command_model import NotificationCreateModel, NotificationCreateResponse
from app.domain.notification.model.notification import Notification
from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.domain.user.model.user_summary import UserSummary
from app.domain.user.repository.user_repository import UserRepository


class NotificationCommandUseCase(ABC):
    """NotificationCommandUseCase defines a command usecase inteface related Notification entity."""

    @abstractmethod
    def create(self, data: NotificationCreateModel, email: str) -> NotificationCreateResponse:
        raise NotImplementedError


class NotificationCommandUseCaseImpl(NotificationCommandUseCase):
    """NotificationCommandUseCaseImpl implements a command usecases related Notification entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            notification_repository: NotificationRepository,
    ):
        self.user_repository: UserRepository = user_repository
        self.notification_repository: NotificationRepository = notification_repository


    def create(self, data: NotificationCreateModel, email: str) -> NotificationCreateResponse:
        try:
            # Récupération de l'utilisateur connecté
            user = self.user_repository.find_by_email(email)

            notification = Notification(
                content=data.content,
                type_notif=TypeNotification.from_str(data.type_notification),
                is_read=data.is_read,
                user=UserSummary(id=user.id, email=user.email),
            )

            # Enregistrement dans la base de données
            self.notification_repository.create(notification)
            self.notification_repository.commit()
        except:
            self.notification_repository.rollback()
            raise

        return NotificationCreateResponse()
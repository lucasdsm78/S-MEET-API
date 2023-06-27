from pydantic import BaseModel, Field

from app.domain.notification.exception.notification_exception import NotificationsNotFoundError


class ErrorMessageNotificationsNotFound(BaseModel):
    detail: str = Field(example=NotificationsNotFoundError.message)
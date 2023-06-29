from pydantic import BaseModel, Field


class NotificationCreateModel(BaseModel):
    """NotificationCreateModel represents a write model to create a notification."""

    content: str = Field(example="Vous avez reçu un message de la part de lucas")
    is_read: bool
    type_notification: str = Field(example='smeet')


class NotificationCreateResponse(BaseModel):
    message: str = "The notification is well created"


class NotificationUpdateResponse(BaseModel):
    message: str = "The notification is well updated"
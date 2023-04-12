from pydantic import BaseModel, Field

from app.domain.chat.message.exception.message_exception import MessagesNotFoundError
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UsersNotFoundError, UserNotFoundError


class ErrorMessageUserEmailAlreadyExists(BaseModel):
    detail: str = Field(example=UserEmailAlreadyExistsError.message)


class ErrorMessageUsersNotFound(BaseModel):
    detail: str = Field(example=UsersNotFoundError.message)


class ErrorMessageUserNotFound(BaseModel):
    detail: str = Field(example=UserNotFoundError.message)


class ErrorMessagesRoomNotFound(BaseModel):
    detail: str = Field(example=MessagesNotFoundError.message)

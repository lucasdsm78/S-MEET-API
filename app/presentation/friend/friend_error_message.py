from pydantic import BaseModel, Field

from app.domain.chat.message.exception.message_exception import MessagesNotFoundError
from app.domain.friend.exception.friend_exception import FriendAlreadyExistsError, FriendsNotFoundError, FriendNotFoundError


class ErrorMessageFriendEmailAlreadyExists(BaseModel):
    detail: str = Field(example=FriendAlreadyExistsError.message)


class ErrorMessageFriendsNotFound(BaseModel):
    detail: str = Field(example=FriendsNotFoundError.message)


class ErrorMessageFriendNotFound(BaseModel):
    detail: str = Field(example=FriendNotFoundError.message)


class ErrorMessagesRoomNotFound(BaseModel):
    detail: str = Field(example=MessagesNotFoundError.message)

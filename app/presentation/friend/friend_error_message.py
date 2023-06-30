from pydantic import BaseModel, Field

from app.domain.friend.exception.friend_exception import FriendAlreadyExistsError, FriendsNotFoundError, FriendNotFoundError


class ErrorMessageFriendAlreadyExists(BaseModel):
    detail: str = Field(example=FriendAlreadyExistsError.message)


class ErrorMessageFriendsNotFound(BaseModel):
    detail: str = Field(example=FriendsNotFoundError.message)


class ErrorMessageFriendNotFound(BaseModel):
    detail: str = Field(example=FriendNotFoundError.message)

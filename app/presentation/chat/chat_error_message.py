from pydantic import BaseModel, Field

from app.domain.chat.message.exception.message_exception import MessageNotFoundError
from app.domain.chat.room.exception.room_exception import RoomNotFoundError, RoomsNotFoundError


class ErrorMessageRoomNotFound(BaseModel):
    detail: str = Field(example=RoomNotFoundError.message)


class ErrorMessageMessageNotFound(BaseModel):
    detail: str = Field(example=MessageNotFoundError.message)


class ErrorMessageRoomsNotFound(BaseModel):
    detail: str = Field(example=RoomsNotFoundError.message)
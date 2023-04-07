from pydantic import Field, BaseModel

from app.domain.chat.message.model.message import Message


class MessageReadModel(BaseModel):
    """MessageReadModel represents data structure as a read model."""

    id: int
    user_id: int = Field(example=1)
    room_id: int = Field(example=1)
    content: str = Field(example="Salut")
    createdAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(message: Message) -> "MessageReadModel":
        return MessageReadModel(
            id=message.id,
            user_id=message.user_id,
            room_id=message.room_id,
            content=message.content,
            createdAt=message.created_at,
        )

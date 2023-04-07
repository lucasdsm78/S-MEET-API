from pydantic import BaseModel, Field


class MessageCreateModel(BaseModel):
    """MessageCreateModel represents a write model to create a message."""

    content: str = Field(example="Salut")
    room_id: int = Field(example=1)


class MessageCreateResponse(BaseModel):
    message: str = "The message is well added"

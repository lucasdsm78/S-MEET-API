from pydantic import BaseModel, Field


class RoomCreateModel(BaseModel):
    """RoomCreateModel represents a write model to create a room."""

    name: str = Field(example="groupe des bg")
    description: str = Field(example="groupe m1 lead dev")
    image_room: str = Field(example="string")
    users: list


class RoomCreateResponse(BaseModel):
    message: str = "The room is well created"


class RoomParticipateResponse(BaseModel):
    message: str = "Your participation for the room is well saved"


class RoomCancelParticipationResponse(BaseModel):
    message: str = "Your participation for the room is well canceled"

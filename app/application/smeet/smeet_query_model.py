from pydantic import Field, BaseModel

from app.domain.smeet.model.smeet import Smeet


class SmeetReadModel(BaseModel):
    """SmeetReadModel represents data structure as a read model."""

    id: int
    user_receiver_id: int
    user_sender_id: int
    content: str = Field(example="Salut ça va ?")
    is_edited: bool
    created_at: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(smeet: Smeet) -> "SmeetReadModel":
        return SmeetReadModel(
            id=smeet.id,
            user_receiver_id=smeet.user_receiver,
            user_sender_id=smeet.user_sender,
            content=smeet.content,
            created_at=smeet.created_at,
            is_edited=smeet.is_edited
        )
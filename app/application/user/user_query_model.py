from pydantic import Field, BaseModel

from app.domain.user.model.user import User


class UserReadModel(BaseModel):
    """UserReadModel represents data structure as a read model."""

    id: int
    email: str = Field(example="lucas@esiee-it.fr")
    first_name: str = Field(example="lucas")
    last_name: str = Field(example="Da Silva")
    pseudo: str = Field(example="lucasdsm")
    createdAt: int = Field(example=1136214245000)
    updatedAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(user: User) -> "UserReadModel":
        return UserReadModel(
            id=user.id,
            email=user.email.value,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
            first_name=user.first_name,
            last_name=user.last_name,
            pseudo=user.pseudo,
        )

from pydantic import Field, BaseModel

from app.domain.friend.model.friend import Friend
from app.domain.user.model.user import User


class FriendReadModel(BaseModel):
    """FriendReadModel represents data structure as a read model."""

    id: int
    first_name: str
    last_name: str
    email: str
    uuid: str
    image_profil: str
    pseudo: str
    createdAt: int
    updatedAt: int
    user_bio_id: int

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(user: User) -> "FriendReadModel":
        return FriendReadModel(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email.value,
            uuid=user.uuid,
            image_profil=user.image_profil,
            createdAt=user.created_at,
            updatedAt=user.updated_at,
            pseudo=user.pseudo,
            user_bio_id=user.user_bio_id
        )

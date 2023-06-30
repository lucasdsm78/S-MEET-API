from pydantic import Field, BaseModel

from app.domain.friend.model.friend import Friend


class FriendReadModel(BaseModel):
    """FriendReadModel represents data structure as a read model."""

    id: int
    id_owner_profile: int = Field(example=0)
    id_second_user: int = Field(example=1)
    is_friend: bool

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(friend: Friend) -> "FriendReadModel":
        return FriendReadModel(
            id=friend.id,
            id_owner_profile=friend.id_owner_profile,
            id_second_user=friend.id_second_user,
            is_friend=friend.is_friend
        )

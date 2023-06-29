from pydantic import BaseModel, Field


class FriendAddModel(BaseModel):
    """FriendAddModel represents a write model to add a friend."""

    id_owner_profile: int = Field(example=0)
    id_second_user: int = Field(example=1)


class FriendAddResponse(BaseModel):
    message: str = "The friend is well added"


class FriendRemoveModel(BaseModel):
    """FriendRemoveModel represents a write model to remove a friend."""

    id: int = Field(example=0)


class FriendRemoveResponse(BaseModel):
    message: str = "The friend is well removed"

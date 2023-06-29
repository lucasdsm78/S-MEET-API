from typing import Optional

from pydantic import BaseModel, Field


class BadgeCreateModel(BaseModel):
    """BadgeCreateModel represents a write model to create a badge."""

    is_default: bool
    name: str
    description: str = Field(example="Avoir participé à la Beta de l'app")
    school_id: int
    icon: str
    is_secret: bool


class BadgeUpdateModel(BaseModel):
    """BadgeUpdateModel represents a write model to update a badge."""

    name: Optional[str]
    description: Optional[str]
    icon: Optional[str]

class BadgeCreateResponse(BaseModel):
    message: str = "The badge is well created"


class BadgeUpdateResponse(BaseModel):
    message: str = "The badge is well updated"


class BadgeDeleteResponse(BaseModel):
    message: str = "The badge is well deleted"
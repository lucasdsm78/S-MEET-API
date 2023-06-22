from pydantic import BaseModel, Field


class UserBioCreateModel(BaseModel):
    """UserBioCreateModel represents a write model to create a user bio."""

    bio: str = Field(example="Bio rapide")
    description: str = Field(example="Description longue")
    birthday: int = Field(example=1136214245000)
    promo: str = Field(example="2B")
    link_instagram: str = Field(example="https://www.instagram.com/example/")
    link_twitter: str = Field(example="https://twitter.com/example")
    link_linkedin: str = Field(example="https://www.linkedin.com/in/example/")


class UserBioCreateResponse(BaseModel):
    message: str = "The bio user is well created"


class UserBioUpdateResponse(BaseModel):
    message: str = "The bio user is well update"

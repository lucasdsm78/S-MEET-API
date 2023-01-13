from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""

    pseudo: str = Field(example="lucasdsm")
    first_name: str = Field(example="Lucas")
    last_name: str = Field(example="Da Silva Marques")
    email: str = Field(example="lucas@esieeit.fr")
    password: str = Field(example="password")
    school: str


class UserCreateResponse(BaseModel):
    message: str = "The user is well created"

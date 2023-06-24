from typing import Optional

from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""

    pseudo: str = Field(example="lucasdsm")
    first_name: str = Field(example="Lucas")
    image_profil: str
    last_name: str = Field(example="Da Silva Marques")
    email: str = Field(example="lucas@esieeit.fr")
    password: str = Field(example="password")
    school: int


class UserCreateResponse(BaseModel):
    message: str = "The user is well created"


class UserDeleteResponse(BaseModel):
    message: str = "The user is well deleted"


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserUpdateModel(BaseModel):
    pseudo: Optional[str]
    image_profil: Optional[str]


class UserLoginResponse(BaseModel):
    token_auth: str = Field(alias="tokenAuth")
    uuid: str = Field()
    token_expiration: str = Field(alias="tokenExpiration")

    def for_login(self):
        return dict(
            tokenAuth=self.token_auth,
            uuid=self.uuid,
            tokenExpiration=self.token_expiration,
            message="login successful"
        )


class InvalidPasswordError(Exception):

    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Password invalid for user {self.email}"

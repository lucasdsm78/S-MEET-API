from pydantic import BaseModel, Field


class UserCreateModel(BaseModel):
    """UserCreateModel represents a write model to create a user."""

    pseudo: str = Field(example="lucasdsm")
    first_name: str = Field(example="Lucas")
    last_name: str = Field(example="Da Silva Marques")
    email: str = Field(example="lucas@esieeit.fr")
    password: str = Field(example="password")
    school: int


class UserCreateResponse(BaseModel):
    message: str = "The user is well created"


class UserLoginModel(BaseModel):
    email: str
    password: str


class UserLoginResponse(BaseModel):
    token_auth: str = Field(alias="tokenAuth")
    token_expiration: str = Field(alias="tokenExpiration")

    def for_login(self):
        return dict(
            tokenAuth=self.token_auth,
            tokenExpiration=self.token_expiration,
            message="login successful"
        )


class InvalidPasswordError(Exception):

    def __init__(self, email: str):
        self.email = email

    def __str__(self):
        return f"Password invalid for user {self.email}"

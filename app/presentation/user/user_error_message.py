from pydantic import BaseModel, Field

from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UsersNotFoundError


class ErrorMessageUserEmailAlreadyExists(BaseModel):
    detail: str = Field(example=UserEmailAlreadyExistsError.message)


class ErrorMessageUsersNotFound(BaseModel):
    detail: str = Field(example=UsersNotFoundError.message)

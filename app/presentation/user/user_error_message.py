from pydantic import BaseModel, Field

from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError


class ErrorMessageUserEmailAlreadyExists(BaseModel):
    detail: str = Field(example=UserEmailAlreadyExistsError.message)

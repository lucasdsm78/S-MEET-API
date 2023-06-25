from pydantic import BaseModel, Field

from app.domain.smeet.exception.smeet_exception import SmeetsNotFoundError


class ErrorMessageSmeetsNotFound(BaseModel):
    detail: str = Field(example=SmeetsNotFoundError.message)
from pydantic import BaseModel, Field

from app.domain.school.exception.school_exception import SchoolNamelAlreadyExistsError


class ErrorMessageSchoolNameAlreadyExists(BaseModel):
    detail: str = Field(example=SchoolNamelAlreadyExistsError.message)

from pydantic import BaseModel, Field

from app.domain.activity.exception.activity_exception import ActivitiesNotFoundError


class ErrorMessageActivitiesNotFound(BaseModel):
    detail: str = Field(example=ActivitiesNotFoundError.message)

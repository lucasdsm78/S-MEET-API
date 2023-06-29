from pydantic import BaseModel, Field

from app.domain.activity.exception.activity_exception import ActivitiesNotFoundError, ActivityNotFoundError, \
    EventsNotFoundError


class ErrorMessageActivitiesNotFound(BaseModel):
    detail: str = Field(example=ActivitiesNotFoundError.message)


class ErrorMessageEventsNotFound(BaseModel):
    detail: str = Field(example=EventsNotFoundError.message)


class ErrorMessageActivityNotFound(BaseModel):
    detail: str = Field(example=ActivityNotFoundError.message)

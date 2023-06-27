from pydantic import BaseModel, Field

from app.domain.badge.exception.badge_exception import BadgesNotFoundError, BadgeNotFoundError


class ErrorMessageBadgesNotFound(BaseModel):
    detail: str = Field(example=BadgesNotFoundError.message)


class ErrorMessageBadgeNotFound(BaseModel):
    detail: str = Field(example=BadgeNotFoundError.message)
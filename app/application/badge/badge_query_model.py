from pydantic import Field, BaseModel

from app.domain.badge.model.badge import Badge
from app.domain.badge.model.properties.user_badge import UserBadge


class BadgeReadModel(BaseModel):
    """BadgeReadModel represents data structure as a read model."""

    id: int
    is_default: bool
    uuid: str
    name: str
    description: str
    icon: str
    is_secret: bool
    createdAt: int = Field(example=1136214245000)
    updatedAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(badge: Badge) -> "BadgeReadModel":
        return BadgeReadModel(
            id=badge.id,
            uuid=badge.uuid,
            is_default=badge.is_default,
            name=badge.name,
            createdAt=badge.created_at,
            updatedAt=badge.updated_at,
            description=badge.description,
            icon=badge.icon,
            is_secret=badge.is_secret,
        )

class UserBadgeReadModel(BaseModel):
    """UserBadgeReadModel represents data structure as a read model."""

    id: int
    grade: str
    badge_id: int
    obtention_date: int

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(user_badge: UserBadge) -> "UserBadgeReadModel":
        return UserBadgeReadModel(
            id=user_badge.id,
            grade=user_badge.grade.value,
            badge_id=user_badge.badge,
            obtention_date=user_badge.created_at
        )
from typing import Optional

from app.domain.badge.model.badge import Badge
from app.domain.badge.model.badge_summary import BadgeSummary
from app.domain.badge.model.properties.grade import Grade
from app.domain.user.model.user_summary import UserSummary


class UserBadge:
    """UserBadge represents your collection of userbadges as an entity."""

    def __init__(
            self,
            badge: int,
            user: int,
            grade: Grade,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.badge: int = badge
        self.user: int = user
        self.grade: Grade = grade
        self.created_at: Optional[int] = created_at
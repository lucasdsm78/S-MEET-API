from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.badge.model.badge import Badge
from app.domain.badge.model.badge_summary import BadgeSummary
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.user.model.email import Email
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBUserBadge(Base):
    """DBUserBadge is a data transfer object associated with UserBadge entity."""

    __tablename__ = "user_badge"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    grade: Union[str, Column] = Column(String, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='userbadges')
    badge_id: Union[int, Column] = Column(Integer, ForeignKey('badge.id'))
    badge = relationship("DBBadge", back_populates='userbadges')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> UserBadge:
        return UserBadge(
            id=self.id,
            grade=Grade.from_str(self.grade),
            user=self.user_id,
            badge=self.badge_id,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(user_badge: UserBadge, db_user_badge: Optional["DBUserBadge"] = None) -> "DBUserBadge":
        now = unixtimestamp()
        user_badge_db_to_update = db_user_badge if db_user_badge is not None else DBUserBadge()
        user_badge_db_to_update.id = user_badge.id
        user_badge_db_to_update.user_id = user_badge.user
        user_badge_db_to_update.badge_id = user_badge.badge
        user_badge_db_to_update.grade = user_badge.grade.value
        user_badge_db_to_update.created_at = now
        return user_badge_db_to_update
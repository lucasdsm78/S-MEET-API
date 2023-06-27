from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from app.domain.badge.model.badge import Badge
from app.domain.user.model.school import School
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBBadge(Base):
    """DBBadge is a data transfer object associated with Badge entity."""

    __tablename__ = "badge"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    is_default: Union[bool, Column] = Column(Boolean, nullable=False)
    is_secret: Union[bool, Column] = Column(Boolean, nullable=False)
    uuid: Union[str, Column] = Column(String, nullable=False, unique=True)
    name: Union[str, Column] = Column(String, nullable=False)
    description: Union[str, Column] = Column(String, nullable=False)
    icon: Union[str, Column] = Column(String, nullable=False)
    school_id: Union[int, Column] = Column(Integer, ForeignKey('school.id'))
    school = relationship("DBSchool", back_populates='badge')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    userbadges = relationship("DBUserBadge", back_populates="badge")

    def to_entity(self) -> Badge:
        return Badge(
            id=self.id,
            uuid=self.uuid,
            is_default=self.is_default,
            is_secret=self.is_secret,
            name=self.name,
            school=School(id=self.school_id, name=self.school.name) if self.school else None,
            icon=self.icon,
            description=self.description,
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_entity(badge: Badge, db_badge: Optional["DBBadge"] = None) -> "DBBadge":
        now = unixtimestamp()
        badge_db_to_update = db_badge if db_badge is not None else DBBadge()
        badge_db_to_update.id = badge.id
        badge_db_to_update.uuid = badge.uuid
        badge_db_to_update.is_default = badge.is_default
        badge_db_to_update.is_secret = badge.is_secret
        badge_db_to_update.name = badge.name
        badge_db_to_update.description = badge.description
        badge_db_to_update.school_id = badge.school.id
        badge_db_to_update.icon = badge.icon
        badge_db_to_update.created_at = now
        badge_db_to_update.updated_at = now
        return badge_db_to_update
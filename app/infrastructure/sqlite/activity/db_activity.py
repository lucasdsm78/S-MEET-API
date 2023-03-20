from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.activity.model.activity import Activity
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.user.model.email import Email
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBActivity(Base):
    """DBActivity is a data transfer object associated with Activity entity."""

    __tablename__ = "activity"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    type: Union[str, Column] = Column(String, nullable=False)
    name: Union[str, Column] = Column(String, nullable=False)
    category: Union[str, Column] = Column(String, nullable=False)
    description: Union[str, Column] = Column(String, nullable=False)
    start_date: Union[int, Column] = Column(Integer, index=True, nullable=False)
    end_date: Union[int, Column] = Column(Integer, index=True, nullable=False)
    place: Union[str, Column] = Column(String, nullable=False)
    image_activity: Union[str, Column] = Column(String, nullable=False)
    max_members: Union[int, Column] = Column(Integer, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='activities')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    activity_participants = relationship("DBActivityParticipants", back_populates="activity")

    def to_entity(self) -> Activity:
        return Activity(
            id=self.id,
            type=Type.from_str(self.type),
            category=Category.from_str(self.category),
            name=self.name,
            image_activity=self.image_activity,
            description=self.description,
            start_date=self.start_date,
            end_date=self.end_date,
            place=self.place,
            max_members=self.max_members,
            user=UserSummary(id=self.user_id, email=Email(self.user.email)),
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(activity: Activity, db_activity: Optional["DBActivity"] = None) -> "DBActivity":
        now = unixtimestamp()
        activity_db_to_update = db_activity if db_activity is not None else DBActivity()
        activity_db_to_update.id = activity.id
        activity_db_to_update.type = activity.type.value
        activity_db_to_update.category = activity.category.value
        activity_db_to_update.name = activity.name
        activity_db_to_update.description = activity.description
        activity_db_to_update.start_date = activity.start_date
        activity_db_to_update.end_date = activity.end_date
        activity_db_to_update.place = activity.place
        activity_db_to_update.image_activity = activity.image_activity
        activity_db_to_update.max_members = activity.max_members
        activity_db_to_update.user_id = activity.user.id
        activity_db_to_update.created_at = now
        activity_db_to_update.updated_at = now
        return activity_db_to_update

from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.activity.model.activity_participants import ActivityParticipant
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBActivityParticipants(Base):
    __tablename__ = "activity_participants"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='activity_participants')
    activity_id: Union[int, Column] = Column(Integer, ForeignKey('activity.id'))
    activity = relationship("DBActivity", back_populates='activity_participants')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> ActivityParticipant:
        return ActivityParticipant(
            id=self.id,
            user_id=self.user_id,
            activity_id=self.activity_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(activity_participant: ActivityParticipant, db_activity_participant:
    Optional["DBActivityParticipants"] = None) -> "DBActivityParticipants":
        now = unixtimestamp()
        activity_participant_db_to_update = db_activity_participant if db_activity_participant \
                                                                       is not None else DBActivityParticipants()
        activity_participant_db_to_update.id = activity_participant.id
        activity_participant_db_to_update.user_id = activity_participant.user_id
        activity_participant_db_to_update.activity_id = activity_participant.activity_id
        activity_participant_db_to_update.created_at = now
        activity_participant_db_to_update.updated_at = now
        return activity_participant_db_to_update

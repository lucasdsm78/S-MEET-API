from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.activity.model.activity import Activity
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.stats.model.stats import Stat
from app.domain.user.model.email import Email
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBStat(Base):
    """DBStat is a data transfer object associated with Stat entity."""

    __tablename__ = "stat"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    messages_send: Union[int, Column] = Column(Integer, nullable=False)
    smeets_send: Union[int, Column] = Column(Integer, nullable=False)
    quiz_created: Union[int, Column] = Column(Integer, nullable=False)
    quiz_played: Union[int, Column] = Column(Integer, nullable=False)
    events_in: Union[int, Column] = Column(Integer, nullable=False)
    activities_in: Union[int, Column] = Column(Integer, nullable=False)
    activities_created: Union[int, Column] = Column(Integer, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='stats')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Stat:
        return Stat(
            id=self.id,
            messages_send=self.messages_send,
            quiz_created=self.quiz_created,
            quiz_played=self.quiz_played,
            smeets_send=self.smeets_send,
            events_in=self.events_in,
            activities_in=self.activities_in,
            activities_created=self.activities_created,
            user=UserSummary(id=self.user_id, email=Email(self.user.email)),
            created_at=self.created_at,
            updated_at=self.updated_at
        )

    @staticmethod
    def from_entity(stat: Stat, db_stat: Optional["DBStat"] = None) -> "DBStat":
        now = unixtimestamp()
        stat_db_to_update = db_stat if db_stat is not None else DBStat()
        stat_db_to_update.id = stat.id
        stat_db_to_update.messages_send = stat.messages_send
        stat_db_to_update.smeets_send = stat.smeets_send
        stat_db_to_update.quiz_created = stat.quiz_created
        stat_db_to_update.quiz_played = stat.quiz_played
        stat_db_to_update.events_in = stat.events_in
        stat_db_to_update.activities_in = stat.activities_in
        stat_db_to_update.activities_created = stat.activities_created
        stat_db_to_update.user_id = stat.user.id
        stat_db_to_update.created_at = now
        stat_db_to_update.updated_at = now
        return stat_db_to_update
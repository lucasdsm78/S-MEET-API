from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.user.model.email import Email
from app.domain.user.model.password import Password
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBUser(Base):
    """DBUser is a data transfer object associated with User entity."""

    __tablename__ = "user"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    email: Union[str, Column] = Column(String(17), unique=True, nullable=False)
    password: Union[str, Column] = Column(String, nullable=True)
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    first_name: Union[str, Column] = Column(String, nullable=False)
    pseudo: Union[str, Column] = Column(String, nullable=False)
    last_name: Union[str, Column] = Column(String, nullable=False)
    school_id: Union[int, Column] = Column(Integer, ForeignKey('school.id'))
    user_bio_id: Union[int, Column] = Column(Integer, ForeignKey('user_bio.id'))
    school = relationship("DBSchool", back_populates='user')
    activities = relationship("DBActivity", back_populates="user")
    quizs = relationship("DBQuiz", back_populates="user")
    messages = relationship("DBMessage", back_populates="user")
    activity_participants = relationship("DBActivityParticipants", back_populates="user")
    room_participants = relationship("DBRoomParticipants", back_populates="user")

    def to_entity(self) -> User:
        return User(
            id=self.id,
            email=Email(self.email),
            password=Password(self.password),
            created_at=self.created_at,
            updated_at=self.updated_at,
            first_name=self.first_name,
            pseudo=self.pseudo,
            last_name=self.last_name,
            user_bio_id=self.user_bio_id,
            school=School(id=self.school_id, name=self.school.name) if self.school else None
        )

    @staticmethod
    def from_entity(user: User, db_user: Optional["DBUser"] = None) -> "DBUser":
        now = unixtimestamp()
        user_db_to_update = db_user if db_user is not None else DBUser()
        user_db_to_update.id = user.id
        user_db_to_update.email = user.email.value
        user_db_to_update.password = user.password.password
        user_db_to_update.created_at = now
        user_db_to_update.updated_at = now
        user_db_to_update.school_id = user.school.id
        user_db_to_update.first_name = user.first_name
        user_db_to_update.last_name = user.last_name
        user_db_to_update.pseudo = user.pseudo
        user_db_to_update.user_bio_id = user.user_bio_id
        return user_db_to_update

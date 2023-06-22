from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.quiz.model.quiz import Quiz
from app.domain.user.model.email import Email
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base
from app.infrastructure.sqlite.quiz.db_question import DBQuestion


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBQuiz(Base):
    """DBQuiz is a data transfer object associated with Quiz entity."""

    __tablename__ = "quiz"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    name: Union[str, Column] = Column(String, nullable=False)
    nbr_questions: Union[int, Column] = Column(Integer, nullable=False)
    image: Union[str, Column] = Column(String, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='quizs')
    questions = relationship("DBQuestion", back_populates='quiz')
    date: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Quiz:
        return Quiz(
            id=self.id,
            name=self.name,
            nbr_questions=self.nbr_questions,
            image=self.image,
            user=UserSummary(id=self.user_id, email=Email(self.user.email)),
            date=self.date,
            questions=self.questions,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(quiz: Quiz, db_quiz: Optional["DBQuiz"] = None) -> "DBQuiz":
        now = unixtimestamp()
        quiz_db_to_update = db_quiz if db_quiz is not None else DBQuiz()
        quiz_db_to_update.id = quiz.id
        quiz_db_to_update.name = quiz.name
        quiz_db_to_update.nbr_questions = quiz.nbr_questions
        quiz_db_to_update.image = quiz.image
        quiz_db_to_update.user_id = quiz.user.id
        quiz_db_to_update.date = now
        quiz_db_to_update.updated_at = now
        return quiz_db_to_update

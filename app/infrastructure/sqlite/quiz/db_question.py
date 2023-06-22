from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.quiz.model.properties.question import Question
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBQuestion(Base):
    """DBQuestion is a data transfer object associated with Question entity."""

    __tablename__ = "question"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    question: Union[str, Column] = Column(String, nullable=False)
    right_answer: Union[str, Column] = Column(String, nullable=False)
    wrong_answer_1: Union[str, Column] = Column(String, nullable=False)
    wrong_answer_2: Union[str, Column] = Column(String, nullable=False)
    wrong_answer_3: Union[str, Column] = Column(String, nullable=False)
    image: Union[str, Column] = Column(String, nullable=False)
    quiz_id: Union[int, Column] = Column(Integer, ForeignKey('quiz.id'))
    quiz = relationship("DBQuiz", back_populates='questions')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)
    updated_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Question:
        return Question(
            id=self.id,
            question=self.question,
            right_answer=self.right_answer,
            wrong_answer_1=self.wrong_answer_1,
            wrong_answer_2=self.wrong_answer_2,
            wrong_answer_3=self.wrong_answer_3,
            image=self.image,
            quiz_id=self.quiz_id,
            created_at=self.created_at,
            updated_at=self.updated_at,
        )

    @staticmethod
    def from_entity(question: Question, db_question: Optional["DBQuestion"] = None) -> "DBQuestion":
        now = unixtimestamp()
        question_db_to_update = db_question if db_question is not None else DBQuestion()
        question_db_to_update.id = question.id
        question_db_to_update.question = question.question
        question_db_to_update.right_answer = question.right_answer
        question_db_to_update.wrong_answer_1 = question.wrong_answer_1
        question_db_to_update.wrong_answer_2 = question.wrong_answer_2
        question_db_to_update.wrong_answer_3 = question.wrong_answer_3
        question_db_to_update.image = question.image
        question_db_to_update.quiz_id = question.quiz_id
        question_db_to_update.created_at = now
        question_db_to_update.updated_at = now
        return question_db_to_update

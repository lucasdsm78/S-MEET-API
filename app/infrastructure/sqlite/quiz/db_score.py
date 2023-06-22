from datetime import datetime
from typing import Union, Optional

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from app.domain.quiz.model.properties.question import Question
from app.domain.quiz.model.properties.score import Score
from app.domain.user.model.email import Email
from app.domain.user.model.user_summary import UserSummary
from app.infrastructure.sqlite.database import Base


def unixtimestamp() -> int:
    return int(datetime.now().timestamp() * 1000)


class DBScore(Base):
    """DBScore is a data transfer object associated with Score entity."""

    __tablename__ = "score"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    score: Union[int, Column] = Column(Integer, nullable=False)
    user_id: Union[int, Column] = Column(Integer, ForeignKey('user.id'))
    user = relationship("DBUser", back_populates='scores')
    quiz_id: Union[int, Column] = Column(Integer, ForeignKey('quiz.id'))
    quiz = relationship("DBQuiz", back_populates='scores')
    created_at: Union[int, Column] = Column(Integer, index=True, nullable=False)

    def to_entity(self) -> Score:
        return Score(
            id=self.id,
            user=UserSummary(id=self.user_id, email=Email(self.user.email)),
            quiz_id=self.quiz_id,
            score=self.score,
            created_at=self.created_at,
        )

    @staticmethod
    def from_entity(score: Score, db_score: Optional["DBScore"] = None) -> "DBScore":
        now = unixtimestamp()
        score_db_to_update = db_score if db_score is not None else DBScore()
        score_db_to_update.id = score.id
        score_db_to_update.quiz_id = score.quiz_id
        score_db_to_update.score = score.score
        score_db_to_update.user_id = score.user.id
        score_db_to_update.created_at = now
        return score_db_to_update

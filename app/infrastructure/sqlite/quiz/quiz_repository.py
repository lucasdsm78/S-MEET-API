from typing import List, Optional

from sqlalchemy.orm.session import Session

from app.domain.quiz.model.quiz import Quiz
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.infrastructure.sqlite.quiz.db_quiz import DBQuiz
from app.infrastructure.sqlite.user.db_user import DBUser


class QuizRepositoryImpl(QuizRepository):
    """QuizRepositoryImpl implements CRUD operations related Quiz entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, quiz: Quiz):
        quiz_db = DBQuiz.from_entity(quiz)
        try:
            self.session.add(quiz_db)
        except:
            raise

    def find_quizs(self, id: int) -> List[Quiz]:
        try:
            quizs_dbs = (
                self.session.query(DBQuiz)
                .join(DBUser)
                .filter(DBQuiz.user_id == id)
                .order_by(DBQuiz.name)
                .all()
            )
        except:
            raise

        if len(quizs_dbs) == 0:
            return []

        return list(map(lambda quiz_db: quiz_db.to_entity(), quizs_dbs))

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

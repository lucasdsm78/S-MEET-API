from typing import List, Optional

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.quiz.exception.quiz_exception import QuizNotFoundError
from app.domain.quiz.model.properties.question import Question
from app.domain.quiz.model.properties.score import Score
from app.domain.quiz.model.quiz import Quiz
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.infrastructure.sqlite.quiz.db_question import DBQuestion
from app.infrastructure.sqlite.quiz.db_quiz import DBQuiz
from app.infrastructure.sqlite.quiz.db_score import DBScore
from app.infrastructure.sqlite.user.db_user import DBUser


class QuizRepositoryImpl(QuizRepository):
    """QuizRepositoryImpl implements CRUD operations related Quiz entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, quiz: Quiz):
        db_quiz = DBQuiz.from_entity(quiz)
        db_questions = [
            DBQuestion.from_entity(question, db_question=DBQuestion())
            for question in quiz.questions
        ]

        db_quiz.questions = db_questions
        self.session.add(db_quiz)
        self.session.flush()

        # Update the quiz_id for the questions
        for db_question in db_questions:
            db_question.quiz_id = db_quiz.id

        return quiz

    def add_score(self, score: Score):
        score_db = DBScore.from_entity(score)
        try:
            self.session.add(score_db)
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

    def find_questions_by_quiz_id(self, quiz_id: int) -> List[Question]:
        try:
            questions_dbs = (
                self.session.query(DBQuestion)
                .join(DBQuiz)
                .filter(DBQuiz.id == quiz_id)
                .all()
            )
        except:
            raise

        if len(questions_dbs) == 0:
            return []

        return list(map(lambda question_db: question_db.to_entity(), questions_dbs))

    def find_by_id(self, quiz_id: int) -> Optional[Quiz]:
        try:
            quiz_db = self.session.query(DBQuiz).filter_by(id=quiz_id).one()
        except NoResultFound:
            raise QuizNotFoundError
        except Exception:
            raise

        return quiz_db.to_entity()

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

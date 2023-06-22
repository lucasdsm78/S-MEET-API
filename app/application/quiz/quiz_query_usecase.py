from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.quiz.quiz_query_model import QuizReadModel, QuestionReadModel
from app.domain.quiz.exception.quiz_exception import ScoreNotFoundError, QuizNotFoundError
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.domain.user.repository.user_repository import UserRepository


class QuizQueryUseCase(ABC):

    @abstractmethod
    def fetch_quizs_by_user_id(self, id: int) -> dict:
        raise NotImplementedError

    def fetch_questions_by_quiz_id(self, quiz_id: int) -> dict:
        raise NotImplementedError

    @abstractmethod
    def fetch_score(self, quiz_id: int, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def fetch_quiz_by_id(self, quiz_id: int) -> Optional[QuizReadModel]:
        raise NotImplementedError


class QuizQueryUseCaseImpl(QuizQueryUseCase, BaseModel):
    quiz_repository: QuizRepository
    user_repository: UserRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_quizs_by_user_id(self, id: int) -> dict:
        try:
            quizs = self.quiz_repository.find_quizs(id)
            return dict(
                quizs=list(map(lambda quiz: QuizReadModel.from_entity_get_all(
                    quiz=quiz), quizs))
            )

        except Exception as e:
            raise

    def fetch_score(self, quiz_id: int, user_id: int) -> int:
        try:
            is_played = self.is_played(quiz_id, user_id)
            if is_played is False:
                raise ScoreNotFoundError
            return self.quiz_repository.get_score(quiz_id, user_id)

        except Exception as e:
            raise

    def fetch_questions_by_quiz_id(self, quiz_id: int) -> dict:
        try:
            questions = self.quiz_repository.find_questions_by_quiz_id(quiz_id)
            return dict(
                questions=list(map(lambda question: QuestionReadModel.from_entity_get_all(
                    question=question), questions))
            )

        except Exception as e:
            raise

    def is_played(self, quiz_id: int, user_id: int) -> bool:
        try:
            user = self.user_repository.find_by_id(user_id)
            quiz = self.quiz_repository.find_by_id(quiz_id)
            is_played = self.quiz_repository.is_played(quiz.id, user.id)
            if is_played is False:
                return False
            return True
        except:
            raise

    def fetch_quiz_by_id(self, quiz_id: int) -> Optional[QuizReadModel]:
        try:
            quiz = self.quiz_repository.find_by_id(quiz_id)
            if quiz is None:
                raise QuizNotFoundError
        except:
            raise

        return QuizReadModel.from_entity_get_all(quiz)
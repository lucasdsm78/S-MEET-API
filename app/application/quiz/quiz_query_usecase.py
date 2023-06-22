from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.quiz.quiz_query_model import QuizReadModel, QuestionReadModel
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.domain.user.repository.user_repository import UserRepository


class QuizQueryUseCase(ABC):

    @abstractmethod
    def fetch_quizs_by_user_id(self, id: int) -> dict:
        raise NotImplementedError

    def fetch_questions_by_quiz_id(self, quiz_id: int) -> dict:
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

    def fetch_questions_by_quiz_id(self, quiz_id: int) -> dict:
        try:
            questions = self.quiz_repository.find_questions_by_quiz_id(quiz_id)
            return dict(
                questions=list(map(lambda question: QuestionReadModel.from_entity_get_all(
                    question=question), questions))
            )

        except Exception as e:
            raise
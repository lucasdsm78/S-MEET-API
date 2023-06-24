from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.activity.model.activity import Activity
from app.domain.quiz.model.properties.question import Question
from app.domain.quiz.model.properties.score import Score
from app.domain.quiz.model.quiz import Quiz


class QuizRepository(ABC):
    """QuizRepository defines a repository interface for Quiz entity."""

    @abstractmethod
    def create(self, quiz: Quiz) -> Optional[Quiz]:
        raise NotImplementedError

    @abstractmethod
    def find_quizs(self, id: int) -> List[Quiz]:
        raise NotImplementedError

    @abstractmethod
    def find_questions_by_quiz_id(self, quiz_id: int) -> List[Question]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, quiz_id: int) -> Optional[Quiz]:
        raise NotImplementedError

    @abstractmethod
    def add_score(self, score: Score) -> Optional[Score]:
        raise NotImplementedError

    @abstractmethod
    def get_score(self, quiz_id: int, user_id: int) -> int:
        raise NotImplementedError

    @abstractmethod
    def is_played(self, quiz_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def delete_quiz(self, quiz_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
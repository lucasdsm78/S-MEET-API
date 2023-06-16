from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse
from app.application.quiz.quiz_command_model import QuizCreateModel, QuizCreateResponse
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.quiz.model.quiz import Quiz
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class QuizCommandUseCase(ABC):
    """QuizCommandUseCase defines a command usecase inteface related Quiz entity."""

    @abstractmethod
    def create(self, email: str, quiz_create_model: QuizCreateModel):
        raise NotImplementedError


class QuizCommandUseCaseImpl(QuizCommandUseCase):
    """QuizCommandUseCaseImpl implements a command usecases related Quiz entity."""

    def __init__(
            self,
            quiz_repository: QuizRepository,
            user_repository: UserRepository,
    ):
        self.quiz_repository: QuizRepository = quiz_repository
        self.user_repository: UserRepository = user_repository

    def create(self, email: str, data: QuizCreateModel) -> QuizCreateResponse:
        try:
            # Récupération de l'utilisateur connecté
            user = self.user_repository.find_by_email(email)

            quiz = Quiz(
                name=data.name,
                nbr_questions=data.nbr_questions,
                image=data.image,
                user=UserSummary(id=user.id, email=user.email),
            )

            # Enregistrement dans la base de données
            self.quiz_repository.create(quiz)
            self.quiz_repository.commit()
        except:
            self.quiz_repository.rollback()
            raise

        return QuizCreateResponse()
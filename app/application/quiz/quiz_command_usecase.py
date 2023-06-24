from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse
from app.application.quiz.quiz_command_model import QuizCreateModel, QuizCreateResponse, ScoreAddedResponse, \
    ScoreCreateModel, QuizDeleteResponse
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.quiz.exception.quiz_exception import QuizNotFoundError
from app.domain.quiz.model.properties.question import Question
from app.domain.quiz.model.properties.score import Score
from app.domain.quiz.model.quiz import Quiz
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class QuizCommandUseCase(ABC):
    """QuizCommandUseCase defines a command usecase inteface related Quiz entity."""

    @abstractmethod
    def create(self, email: str, quiz_create_model: QuizCreateModel):
        raise NotImplementedError

    @abstractmethod
    def add_score(self, user_id: int, id_quiz: int, score: ScoreCreateModel) -> ScoreAddedResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_quiz(self, quiz_id: int) -> QuizDeleteResponse:
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
            questions = []

            for question in data.questions:
                question_new = Question.create(
                    quiz_id=0,
                    question=question.question,
                    right_answer=question.right_answer,
                    wrong_answer_1=question.wrong_answer_1,
                    wrong_answer_2=question.wrong_answer_2,
                    wrong_answer_3=question.wrong_answer_3,
                    image=question.image
                )
                questions.append(question_new)

            quiz = Quiz(
                name=data.name,
                nbr_questions=data.nbr_questions,
                image=data.image,
                user=UserSummary(id=user.id, email=user.email),
                questions=questions
            )

            # Save the Quiz entity and update the quiz_id for the questions
            saved_quiz = self.quiz_repository.create(quiz)
            for question_entity in saved_quiz.questions:
                question_entity.quiz_id = saved_quiz.id

            self.quiz_repository.commit()
        except:
            self.quiz_repository.rollback()
            raise

        return QuizCreateResponse()

    def add_score(self, user_id: int, id_quiz: int, data: ScoreCreateModel) -> ScoreAddedResponse:
        try:
            # Récupération de l'utilisateur connecté
            user = self.user_repository.find_by_id(user_id)

            # Récupération du quiz s'il existe
            quiz = self.quiz_repository.find_by_id(id_quiz)

            score = Score(
                quiz_id=quiz.id,
                score=data.score,
                user=UserSummary(id=user.id, email=user.email),
            )

            self.quiz_repository.add_score(score)
            self.quiz_repository.commit()
        except:
            self.quiz_repository.rollback()
            raise

        return ScoreAddedResponse()

    def delete_quiz(self, quiz_id: int) -> QuizDeleteResponse:
        try:
            existing_quiz = self.quiz_repository.find_by_id(quiz_id)
            if existing_quiz is None:
                raise QuizNotFoundError

            self.quiz_repository.delete_quiz(quiz_id)
            self.quiz_repository.commit()
        except:
            self.quiz_repository.rollback()
            raise

        return QuizDeleteResponse()

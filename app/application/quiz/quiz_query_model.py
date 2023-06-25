from pydantic import Field, BaseModel

from app.domain.quiz.model.properties.question import Question
from app.domain.quiz.model.quiz import Quiz


class QuizReadModel(BaseModel):
    """QuizReadModel represents data structure as a read model."""

    id: int
    uuid: str = Field(example="kiuyueicioe")
    name: str
    creator_id: int
    nbr_questions: int
    image: str = Field(example="images/quiz/1/image.png")
    date: int = Field(example=1136214245000)
    updatedAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity_get_all(quiz: Quiz) -> "QuizReadModel":
        return QuizReadModel(
            id=quiz.id,
            uuid=quiz.uuid,
            name=quiz.name,
            creator_id=quiz.user.id,
            nbr_questions=quiz.nbr_questions,
            image=quiz.image,
            date=quiz.date,
            updatedAt=quiz.updated_at
        )


class QuestionReadModel(BaseModel):
    """QuestionReadModel represents data structure as a read model."""

    id: int
    quiz_id: int
    question: str
    right_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    wrong_answer_3: str
    image: str
    created_at: int

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity_get_all(question: Question) -> "QuestionReadModel":
        return QuestionReadModel(
            id=question.id,
            quiz_id=question.quiz_id,
            question=question.question,
            right_answer=question.right_answer,
            wrong_answer_1=question.wrong_answer_1,
            wrong_answer_2=question.wrong_answer_2,
            wrong_answer_3=question.wrong_answer_3,
            image=question.image,
            created_at=question.created_at,
            updated_at=question.updated_at
        )

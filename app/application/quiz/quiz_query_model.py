from pydantic import Field, BaseModel

from app.domain.quiz.model.quiz import Quiz


class QuizReadModel(BaseModel):
    """QuizReadModel represents data structure as a read model."""

    id: int
    name: str
    creator_id: int
    nbr_questions: int
    image: str
    date: int = Field(example=1136214245000)
    updatedAt: int = Field(example=1136214245000)

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity_get_all(quiz: Quiz) -> "QuizReadModel":
        return QuizReadModel(
            id=quiz.id,
            name=quiz.name,
            creator_id=quiz.user.id,
            nbr_questions=quiz.nbr_questions,
            image=quiz.image,
            date=quiz.date,
            updatedAt=quiz.updated_at
        )
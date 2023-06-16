from pydantic import BaseModel, Field


class QuizCreateModel(BaseModel):
    """QuizCreateModel represents a write model to create a quizz."""

    name: str = Field(example="Quiz personnalité")
    nbr_questions: int
    image: str


class QuizCreateResponse(BaseModel):
    message: str = "The quiz is well created"

from typing import List

from pydantic import BaseModel, Field

from app.domain.quiz.model.properties.question import Question


class QuizCreateModel(BaseModel):
    """QuizCreateModel represents a write model to create a quizz."""

    name: str = Field(example="Quiz personnalité")
    nbr_questions: int
    image: str
    questions: List[Question]


class QuizCreateResponse(BaseModel):
    message: str = "The quiz is well created"

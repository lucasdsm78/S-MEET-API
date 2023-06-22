from typing import List

from pydantic import BaseModel, Field

from app.domain.quiz.model.properties.question import Question


class QuestionCreateModel(BaseModel):
    """Question represents your collection of questions as an entity."""

    question: str
    right_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    wrong_answer_3: str
    image: str


class QuizCreateModel(BaseModel):
    """QuizCreateModel represents a write model to create a quizz."""

    name: str = Field(example="Quiz personnalité")
    nbr_questions: int
    image: str
    questions: List[QuestionCreateModel]


class QuizCreateResponse(BaseModel):
    message: str = "The quiz is well created"

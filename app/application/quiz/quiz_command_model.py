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


class ScoreCreateModel(BaseModel):
    """ScoreCreateModel represents a write model to create a score."""

    score: int


class QuizCreateResponse(BaseModel):
    message: str = "The quiz is well created"


class QuizDeleteResponse(BaseModel):
    message: str = "The quiz is well deleted"


class ScoreAddedResponse(BaseModel):
    message: str = "The score is well added for this quiz and this user"

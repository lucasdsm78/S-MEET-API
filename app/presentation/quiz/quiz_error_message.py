from pydantic import BaseModel, Field

from app.domain.quiz.exception.quiz_exception import QuizsNotFoundError, QuizNotFoundError, ScoreNotFoundError


class ErrorMessageQuizsNotFound(BaseModel):
    detail: str = Field(example=QuizsNotFoundError.message)


class ErrorMessageQuestionsNotFound(BaseModel):
    detail: str = Field(example=QuizsNotFoundError.message)


class ErrorMessageQuizNotFound(BaseModel):
    detail: str = Field(example=QuizNotFoundError.message)


class ErrorMessageScoreNotFound(BaseModel):
    detail: str = Field(example=ScoreNotFoundError.message)

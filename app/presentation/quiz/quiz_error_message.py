from pydantic import BaseModel, Field

from app.domain.quiz.exception.quiz_exception import QuizsNotFoundError, QuizNotFoundError


class ErrorMessageQuizsNotFound(BaseModel):
    detail: str = Field(example=QuizsNotFoundError.message)


class ErrorMessageQuizNotFound(BaseModel):
    detail: str = Field(example=QuizNotFoundError.message)

from typing import Optional

from pydantic import BaseModel


class Question(BaseModel):
    """Question represents your collection of questions as an entity."""

    quiz_id: int
    question: str
    right_answer: str
    wrong_answer_1: str
    wrong_answer_2: str
    wrong_answer_3: str
    image: str
    id: Optional[int] = None
    created_at: Optional[int] = None
    updated_at: Optional[int] = None

    class Config():
        orm_mode = True

    @classmethod
    def create(
            cls,
            quiz_id: int,
            question: str,
            right_answer,
            wrong_answer_1,
            wrong_answer_2,
            wrong_answer_3,
            image: str
    ):
        return cls(
            quiz_id=quiz_id,
            question=question,
            right_answer=right_answer,
            wrong_answer_1=wrong_answer_1,
            wrong_answer_2=wrong_answer_2,
            wrong_answer_3=wrong_answer_3,
            image=image
        )

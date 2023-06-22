from typing import Optional

from pydantic import BaseModel

from app.domain.user.model.user_summary import UserSummary


class Score(BaseModel):
    """Score represents your collection of score as an entity."""

    quiz_id: int
    score: int
    user: UserSummary
    id: Optional[int] = None
    created_at: Optional[int] = None

    class Config():
        orm_mode = True
        arbitrary_types_allowed = True

    @classmethod
    def create(
            cls,
            quiz_id: int,
            score: int,
            user: UserSummary
    ):
        return cls(
            quiz_id=quiz_id,
            score=score,
            user=user
        )

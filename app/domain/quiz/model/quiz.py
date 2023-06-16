from typing import Optional

from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type

from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary


class Quiz:
    """Quiz represents your collection of quizs as an entity."""

    def __init__(
            self,
            name: str,
            nbr_questions: int,
            image: str,
            user: UserSummary,
            id: Optional[int] = None,
            date: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.name: str = name
        self.nbr_questions: int = nbr_questions
        self.image: str = image
        self.user: UserSummary = user
        self.date: Optional[int] = date
        self.updated_at: Optional[int] = updated_at
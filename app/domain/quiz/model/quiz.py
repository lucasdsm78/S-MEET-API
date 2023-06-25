from typing import Optional, List

from app.domain.user.model.user_summary import UserSummary

from app.domain.quiz.model.properties.question import Question


class Quiz:
    """Quiz represents your collection of quizs as an entity."""

    def __init__(
            self,
            name: str,
            uuid: str,
            nbr_questions: int,
            image: str,
            user: UserSummary,
            questions: List[Question],
            id: Optional[int] = None,
            date: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.name: str = name
        self.uuid: str = uuid
        self.nbr_questions: int = nbr_questions
        self.image: str = image
        self.user: UserSummary = user
        self.questions: List[Question] = questions
        self.date: Optional[int] = date
        self.updated_at: Optional[int] = updated_at

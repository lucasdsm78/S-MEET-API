from typing import Optional

from app.domain.activity.model.type import Type

from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary


class Activity:
    """Activity represents your collection of activities as an entity."""

    def __init__(
            self,
            type: Type,
            name: str,
            description: str,
            more: str,
            start_date: int,
            end_date: int,
            place: str,
            max_members: int,
            user: UserSummary,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.type: Type = type
        self.name: str = name
        self.description: str = description
        self.more: str = more
        self.start_date: int = start_date
        self.end_date: int = end_date
        self.place: str = place
        self.user: UserSummary = user
        self.max_members: int = max_members
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
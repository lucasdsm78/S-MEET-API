from typing import Optional

from app.domain.user.model.user_summary import UserSummary


class Stat:
    """Stat represents your collection of stat as an entity."""

    def __init__(
            self,
            messages_send: int,
            smeets_send: int,
            quiz_created: int,
            quiz_played: int,
            user: UserSummary,
            events_in: int,
            activities_in: int,
            activities_created: int,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.messages_send: int = messages_send
        self.smeets_send: int = smeets_send
        self.quiz_created: int = quiz_created
        self.quiz_played: int = quiz_played
        self.user: UserSummary = user
        self.events_in: int = events_in
        self.activities_in: int = activities_in
        self.activities_created: int = activities_created
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

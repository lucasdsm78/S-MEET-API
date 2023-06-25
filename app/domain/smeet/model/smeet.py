from typing import Optional

from app.domain.user.model.user_summary import UserSummary


class Smeet:
    """Smeet represents your collection of smeets as an entity."""

    def __init__(
            self,
            user_receiver: int,
            user_sender: int,
            content: str,
            is_edited: bool,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.content: str = content
        self.user_receiver: int = user_receiver
        self.user_sender: int = user_sender
        self.is_edited: bool = is_edited
        self.created_at: Optional[int] = created_at

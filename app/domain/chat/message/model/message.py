from typing import Optional, List


class Message:
    """Room represents your collection of rooms as an entity."""

    def __init__(
            self,
            content: str,
            room_id: int,
            user_id: int,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.user_id = user_id
        self.room_id = room_id
        self.content = content
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

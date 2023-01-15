from typing import Optional


class ActivityParticipant:

    def __init__(
            self,
            user_id: int,
            activity_id: int,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.user_id: int = user_id
        self.activity_id: int = activity_id
        self.id: Optional[int] = id
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

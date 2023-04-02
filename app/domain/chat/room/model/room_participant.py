from typing import Optional


class RoomParticipant:

    def __init__(
            self,
            user_id: int,
            room_id: int,
            id: Optional[int] = None
    ):
        self.user_id: int = user_id
        self.room_id: int = room_id
        self.id: Optional[int] = id

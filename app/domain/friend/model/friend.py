from typing import Optional


class Friend:
    """Friend represents your collection of friends as an entity."""

    def __init__(
            self,
            id_owner_profile: int,
            id_second_user: int,
            is_friend: bool,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.id_owner_profile: int = id_owner_profile
        self.id_second_user: int = id_second_user
        self.is_friend: bool = is_friend
        self.created_at: Optional[int] = created_at
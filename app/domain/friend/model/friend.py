from typing import Optional


class Friend:
    """Friend represents your collection of friends as an entity."""

    def __init__(
            self,
            id_owner_profile: int,
            id_second_user: int,
            id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.id_owner_profile: int = id_owner_profile
        self.id_second_user: int = id_second_user

    @classmethod
    def create(cls, id_second_user: int = None, id_owner_profile: int = None) -> "Friend":
        return cls(
            id_owner_profile=id_owner_profile,
            id_second_user=id_second_user
        )

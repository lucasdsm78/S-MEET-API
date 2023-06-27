from typing import Optional

from app.domain.user.model.school import School


class Badge:
    """Badge represents your collection of badges as an entity."""

    def __init__(
            self,
            is_default: bool,
            uuid: str,
            name: str,
            school: School,
            description: str,
            icon: str,
            is_secret: bool,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.uuid: str = uuid
        self.name: str = name
        self.description: str = description
        self.icon: str = icon
        self.school: School = school
        self.is_default: bool = is_default
        self.is_secret: bool = is_secret
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at
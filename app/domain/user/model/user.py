from typing import Optional

from app.domain.user.model.email import Email
from app.domain.user.model.password import Password

from app.domain.user.model.school import School


class User:
    """User represents your collection of users as an entity."""

    def __init__(
            self,
            email: Email,
            pseudo: str,
            first_name: str,
            last_name: str,
            school: School,
            password: Password,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.password: Password = password
        self.email: Email = email
        self.created_at: Optional[int] = created_at
        self.school: School = school
        self.pseudo: str = pseudo
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.updated_at: Optional[int] = updated_at

    def token_details(self) -> dict:
        return dict(
            email=self.email.value,
            pseudo=self.pseudo,
            first_name=self.first_name,
            last_name=self.last_name,
            school=self.school.name
        )
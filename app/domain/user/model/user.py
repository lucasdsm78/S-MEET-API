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
            image_profil: str,
            uuid: str,
            first_name: str,
            last_name: str,
            school: School,
            password: Password,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None,
            user_bio_id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.password: Password = password
        self.uuid: str = uuid
        self.email: Email = email
        self.image_profil = image_profil
        self.created_at: Optional[int] = created_at
        self.school: School = school
        self.pseudo: str = pseudo
        self.first_name: str = first_name
        self.last_name: str = last_name
        self.updated_at: Optional[int] = updated_at
        self.user_bio_id: Optional[int] = user_bio_id

    def token_details(self) -> dict:
        return dict(
            email=self.email.value,
            uuid=self.uuid,
            image_profil=self.image_profil,
            pseudo=self.pseudo,
            first_name=self.first_name,
            last_name=self.last_name,
            school_id=self.school.id,
            id=self.id
        )
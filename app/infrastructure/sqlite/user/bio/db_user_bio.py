from typing import Union, Optional

from sqlalchemy import Column, Integer, String

from app.domain.user.model.user_bio import UserBio
from app.infrastructure.sqlite.database import Base


class DBUserBio(Base):
    """DBUserBio is a data transfer object associated with UserBio entity."""

    __tablename__ = "user_bio"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    bio: Union[str, Column] = Column(String, nullable=True)
    description: Union[str, Column] = Column(String, nullable=True)
    birthday: Union[int, Column] = Column(Integer, nullable=True)
    promo: Union[str, Column] = Column(String, nullable=True)
    link_instagram: Union[str, Column] = Column(String, nullable=True)
    link_twitter: Union[str, Column] = Column(String, nullable=True)
    link_linkedin: Union[str, Column] = Column(String, nullable=True)

    def to_entity(self) -> UserBio:
        return UserBio(
            id=self.id,
            bio=self.bio,
            description=self.description,
            birthday=self.birthday,
            promo=self.promo,
            link_instagram=self.link_instagram,
            link_twitter=self.link_twitter,
            link_linkedin=self.link_linkedin
        )

    @staticmethod
    def from_entity(user_bio: UserBio, db_user_bio: Optional["DBUserBio"] = None) -> "DBUserBio":
        user_bio_db_to_update = db_user_bio if db_user_bio is not None else DBUserBio()
        user_bio_db_to_update.id = user_bio.id
        user_bio_db_to_update.bio = user_bio.bio
        user_bio_db_to_update.description = user_bio.description
        user_bio_db_to_update.birthday = user_bio.birthday
        user_bio_db_to_update.promo = user_bio.promo
        user_bio_db_to_update.link_instagram = user_bio.link_instagram
        user_bio_db_to_update.link_twitter = user_bio.link_twitter
        user_bio_db_to_update.link_linkedin = user_bio.link_linkedin
        return user_bio_db_to_update

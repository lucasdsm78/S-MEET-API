from typing import Optional

from pydantic import Field, BaseModel

from app.domain.user.model.user_bio import UserBio


class UserBioReadModel(BaseModel):
    """UserBioReadModel represents data structure as a read model."""

    id: int
    bio: Optional[str] = Field(example="Bio rapide")
    description: Optional[str] = Field(example="Description longue")
    birthday: Optional[int] = Field(example=1136214245000)
    promo: Optional[str] = Field(example="2B")
    link_instagram: Optional[str] = Field(example="https://www.instagram.com/example/")
    link_twitter: Optional[str] = Field(example="https://twitter.com/example")
    link_linkedin: Optional[str] = Field(example="https://www.linkedin.com/in/example/")

    class Config:
        arbitrary_types_allowed = True

    @staticmethod
    def from_entity(user_bio: UserBio) -> "UserBioReadModel":
        return UserBioReadModel(
            id=user_bio.id,
            bio=user_bio.bio if user_bio.bio else None,
            description=user_bio.description if user_bio.description else None,
            birthday=user_bio.birthday if user_bio.birthday else None,
            promo=user_bio.promo if user_bio.promo else None,
            link_instagram=user_bio.link_instagram if user_bio.link_instagram else None,
            link_twitter=user_bio.link_twitter if user_bio.link_twitter else None,
            link_linkedin=user_bio.link_linkedin if user_bio.link_linkedin else None,
        )

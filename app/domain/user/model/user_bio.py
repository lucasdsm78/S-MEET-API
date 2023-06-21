from typing import Optional


class UserBio:
    """UserBio represents your collection of users as an entity."""

    def __init__(
            self,
            bio: Optional[str] = None,
            description: Optional[str] = None,
            birthday: Optional[int] = None,
            promo: Optional[str] = None,
            link_instagram: Optional[str] = None,
            link_twitter: Optional[str] = None,
            link_linkedin: Optional[str] = None,
            id: Optional[int] = None
    ):
        self.id: Optional[int] = id
        self.bio: Optional[str] = bio
        self.description: Optional[str] = description
        self.birthday: Optional[int] = birthday
        self.promo: Optional[str] = promo
        self.link_instagram: Optional[str] = link_instagram
        self.link_twitter: Optional[str] = link_twitter
        self.link_linkedin: Optional[str] = link_linkedin

    @classmethod
    def create(cls, bio: Optional[str] = None, description: Optional[str] = None,
               birthday: Optional[int] = None, promo: Optional[str] = None,
               link_instagram: Optional[str] = None, link_twitter: Optional[str] = None,
               link_linkedin: Optional[str] = None) -> "UserBio":
        return cls(
            bio=bio,
            description=description,
            birthday=birthday,
            promo=promo,
            link_instagram=link_instagram,
            link_twitter=link_twitter,
            link_linkedin=link_linkedin
        )

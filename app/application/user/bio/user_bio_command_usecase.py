from abc import ABC, abstractmethod

from app.application.user.bio.user_bio_command_model import UserBioCreateModel, UserBioUpdateResponse
from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.repository.user_repository import UserRepository


class UserBioCommandUseCase(ABC):
    """UserBioCommandUseCase defines a command usecase inteface related UserBio entity."""

    @abstractmethod
    def update(self, user_id: int, user_bio_create_model: UserBioCreateModel) -> UserBioUpdateResponse:
        raise NotImplementedError


class UserBioCommandUseCaseImpl(UserBioCommandUseCase):
    """UserBioCommandUseCaseImpl implements a command usecases related UserBio entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            user_bio_repository: UserBioRepository
    ):
        self.user_repository: UserRepository = user_repository
        self.user_bio_repository: UserBioRepository = user_bio_repository

    def update(self, user_id: int, data: UserBioCreateModel) -> UserBioUpdateResponse:
        try:
            user_bio = self.user_bio_repository.find_bio_by_user_id(user_id)

            user_bio.bio = data.bio
            user_bio.description = data.description
            user_bio.birthday = data.birthday
            user_bio.promo = data.promo
            user_bio.link_instagram = data.link_instagram
            user_bio.link_twitter = data.link_twitter
            user_bio.link_linkedin = data.link_linkedin

            self.user_bio_repository.update(user_bio)
            self.user_bio_repository.commit()

        except:
            self.user_bio_repository.rollback()
            raise

        return UserBioUpdateResponse()

from abc import ABC, abstractmethod
from typing import Optional

import shortuuid
from fastapi import UploadFile

from app.application.user.user_command_model import UserCreateModel, UserLoginModel, \
    UserLoginResponse, InvalidPasswordError, UserDeleteResponse, UserUpdateModel
from app.application.user.user_query_model import UserReadModel
from app.domain.badge.model.badge_summary import BadgeSummary
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.notification.model.notification import Notification
from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.services.file_uploader.file_uploader import FileUploader
from app.domain.services.hash import Hash
from app.domain.services.manager_token import ManagerToken
from app.domain.stats.model.stats import Stat
from app.domain.stats.repository.stat_repository import StatRepository
from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UserLoginNotFoundError, \
    UserNotFoundError

from app.domain.user.model.email import Email
from app.domain.user.model.password import Password
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from app.domain.user.bio.model.user_bio import UserBio
from app.domain.user.model.user_summary import UserSummary
from app.domain.user.repository.user_repository import UserRepository


class UserCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create(self, user_create_model: UserCreateModel) -> UserLoginResponse:
        raise NotImplementedError

    @abstractmethod
    def login(self, user_login_model: UserLoginModel) -> UserLoginResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_user(self, user_id: int) -> UserDeleteResponse:
        raise NotImplementedError

    @abstractmethod
    def update_user(self, id: int, pseudo: str, image: UploadFile) -> Optional[UserReadModel]:
        raise NotImplementedError


class UserCommandUseCaseImpl(UserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            school_repository: SchoolRepository,
            user_bio_repository: UserBioRepository,
            hasher: Hash,
            manager_token: ManagerToken,
            file_uploader: FileUploader,
            badge_repository: BadgeRepository,
            stat_repository: StatRepository,
            notification_repository: NotificationRepository
    ):
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository
        self.user_bio_repository: UserBioRepository = user_bio_repository
        self.hasher = hasher
        self.manager_token = manager_token
        self.file_uploader = file_uploader
        self.badge_repository: BadgeRepository = badge_repository
        self.stat_repository: StatRepository = stat_repository
        self.notification_repository: NotificationRepository = notification_repository

    def create(self, data: UserCreateModel) -> UserLoginResponse:
        try:
            school = self.school_repository.find_by_id(data.school)

            user_bio = UserBio().create()
            self.user_bio_repository.create(user_bio)
            self.user_bio_repository.commit()

            user_bio_id = self.user_bio_repository.last()

            uuid = shortuuid.uuid()

            email = Email(data.email)
            user = User(
                email=email,
                pseudo=data.pseudo,
                uuid=uuid,
                image_profil=f"images/user/{uuid}/{data.image_profil}",
                first_name=data.first_name,
                last_name=data.last_name,
                school=School(name=school.name, id=school.id),
                password=Password(self.hasher.bcrypt(data.password)),
                user_bio_id=user_bio_id
            )

            existing_user = self.user_repository.find_by_email(data.email)
            if existing_user is not None:
                raise UserEmailAlreadyExistsError

            self.user_repository.create(user)
            self.user_repository.commit()

            user = self.user_repository.find_by_email(data.email)
            if not user:
                raise UserLoginNotFoundError(data.email)

            badge = self.badge_repository.find_by_name('Beta testeur')
            grade = Grade.from_str('bronze')

            user_badge = UserBadge(
                badge=badge.id,
                user=user.id,
                grade=grade
            )

            self.badge_repository.add_badge_to_user(user_badge)

            notification = Notification(
                content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez participé à la béta de l'application",
                is_read=False,
                type_notif=TypeNotification.from_str('beta'),
                user=UserSummary(id=user.id, email=user.email),
            )

            self.notification_repository.create(notification)

            self.badge_repository.commit()
            self.notification_repository.commit()

            stat = Stat(
                messages_send=0,
                smeets_send=0,
                quiz_created=0,
                quiz_played=0,
                user=UserSummary(email=user.email, id=user.id),
                events_in=0,
                activities_in=0,
                activities_created=0
            )
            self.stat_repository.create(stat)
            self.stat_repository.commit()

        except:
            self.user_repository.rollback()
            self.badge_repository.rollback()
            self.stat_repository.rollback()
            self.notification_repository.rollback()
            raise

        return UserLoginResponse(
            uuid=user.uuid,
            tokenAuth=self.manager_token.generate_token_login(user),
            tokenExpiration=self.manager_token.generate_expiration_token_login(user),
        )

    def login(self, user_login_model: UserLoginModel) -> UserLoginResponse:
        user = self.user_repository.find_by_email(user_login_model.email)
        if not user:
            raise UserLoginNotFoundError(user_login_model.email)
        if not self.hasher.verify(user.password.password, user_login_model.password):
            raise InvalidPasswordError(user_login_model.email)

        return UserLoginResponse(
            uuid=user.uuid,
            tokenAuth=self.manager_token.generate_token_login(user),
            tokenExpiration=self.manager_token.generate_expiration_token_login(user),
        )

    def delete_user(self, user_id: int) -> UserDeleteResponse:
        try:
            existing_user = self.user_repository.find_by_id(user_id)
            if existing_user is None:
                raise UserNotFoundError

            self.user_repository.delete_user(user_id)
            self.user_repository.commit()
        except:
            self.user_repository.rollback()
            raise

        return UserDeleteResponse()

    def update_user(self, id: int, pseudo: str, image: UploadFile) -> Optional[UserReadModel]:
        try:
            existing_user = self.user_repository.find_by_id(id)
            if existing_user is None:
                raise UserNotFoundError

            if pseudo is not None:
                existing_user.pseudo = pseudo

            if image is not None:
                self.file_uploader.delete_image_file('user')
                self.file_uploader.save_image_file('user', image, existing_user.uuid)
                existing_user.image_profil = f"images/user/{existing_user.uuid}/{image.filename}"

            self.user_repository.update_user(existing_user)
            updated_user = self.user_repository.find_by_id(existing_user.id)
            self.user_repository.commit()
        except:
            self.user_repository.rollback()
            raise

        return UserReadModel.from_entity(updated_user)

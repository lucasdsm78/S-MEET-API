from abc import ABC, abstractmethod
from typing import Optional

import shortuuid

from app.application.user.user_command_model import UserCreateModel, UserLoginModel, \
    UserLoginResponse, InvalidPasswordError, UserDeleteResponse, UserUpdateModel
from app.application.user.user_query_model import UserReadModel
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.services.hash import Hash
from app.domain.services.manager_token import ManagerToken
from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UserLoginNotFoundError, \
    UserNotFoundError

from app.domain.user.model.email import Email
from app.domain.user.model.password import Password
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from app.domain.user.bio.model.user_bio import UserBio
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
    def update_user(self, id: int, data: UserUpdateModel) -> Optional[UserReadModel]:
        raise NotImplementedError


class UserCommandUseCaseImpl(UserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            school_repository: SchoolRepository,
            user_bio_repository: UserBioRepository,
            hasher: Hash,
            manager_token: ManagerToken
    ):
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository
        self.user_bio_repository: UserBioRepository = user_bio_repository
        self.hasher = hasher
        self.manager_token = manager_token

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

        except:
            self.user_repository.rollback()
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

    def update_user(self, id: int, data: UserUpdateModel) -> Optional[UserReadModel]:
        try:
            existing_user = self.user_repository.find_by_id(id)
            if existing_user is None:
                raise UserNotFoundError

            if data.pseudo is not None:
                existing_user.pseudo = data.pseudo

            if data.image_profil is not None:
                existing_user.image_profil = data.image_profil

            self.user_repository.update_user(existing_user)
            updated_user = self.user_repository.find_by_id(existing_user.id)
            self.user_repository.commit()
        except:
            self.user_repository.rollback()
            raise

        return UserReadModel.from_entity(updated_user)

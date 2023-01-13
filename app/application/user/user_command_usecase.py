from abc import ABC, abstractmethod

from app.application.user.user_command_model import UserCreateModel, UserCreateResponse
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError

from app.domain.user.model.email import Email
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from db.hash import Hash
from app.domain.user.repository.user_repository import UserRepository


class UserCommandUseCase(ABC):
    """UserCommandUseCase defines a command usecase inteface related User entity."""

    @abstractmethod
    def create(self, user_create_model: UserCreateModel):
        raise NotImplementedError


class UserCommandUseCaseImpl(UserCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            user_repository: UserRepository,
            school_repository: SchoolRepository
    ):
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository

    def create(self, data: UserCreateModel) -> UserCreateResponse:
        try:
            school = self.school_repository.find_by_name(data.school)

            email = Email(data.email)
            user = User(
                email=email,
                pseudo=data.pseudo,
                first_name=data.first_name,
                last_name=data.last_name,
                school=School(school.name),
                password=Hash.bcrypt(data.password))

            existing_user = self.user_repository.find_by_email(data.email)
            if existing_user is not None:
                raise UserEmailAlreadyExistsError

            self.user_repository.create(user)
            self.user_repository.commit()

        except:
            self.user_repository.rollback()
            raise

        return UserCreateResponse()

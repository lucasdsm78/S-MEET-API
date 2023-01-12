from abc import ABC, abstractmethod

from app.application.school.school_command_model import SchoolCreateModel, SchoolCreateResponse
from app.domain.school.exception.school_exception import SchoolNamelAlreadyExistsError
from app.domain.school.repository.school_repository import SchoolRepository

from app.domain.user.model.school import School


class SchoolCommandUseCase(ABC):
    """SchoolCommandUseCase defines a command usecase inteface related School entity."""

    @abstractmethod
    def create(self, school_create_model: SchoolCreateModel):
        raise NotImplementedError


class SchoolCommandUseCaseImpl(SchoolCommandUseCase):
    """UserCommandUseCaseImpl implements a command usecases related User entity."""

    def __init__(
            self,
            school_repository: SchoolRepository,
    ):
        self.school_repository: SchoolRepository = school_repository

    def create(self, data: SchoolCreateModel) -> SchoolCreateResponse:
        try:
            school = School(
                name=data.name)

            existing_school = self.school_repository.find_by_name(data.name)
            if existing_school is not None:
                raise SchoolNamelAlreadyExistsError

            self.school_repository.create(school)
            self.school_repository.commit()
        except:
            self.school_repository.rollback()
            raise

        return SchoolCreateResponse()
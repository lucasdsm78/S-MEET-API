from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse
from app.domain.activity.model.activity import Activity
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class ActivityCommandUseCase(ABC):
    """ActivityCommandUseCase defines a command usecase inteface related Activity entity."""

    @abstractmethod
    def create(self, activity_create_model: ActivityCreateModel):
        raise NotImplementedError


class ActivityCommandUseCaseImpl(ActivityCommandUseCase):
    """ActivityCommandUseCaseImpl implements a command usecases related Activity entity."""

    def __init__(
            self,
            activity_repository: ActivityRepository,
            user_repository: UserRepository,
    ):
        self.activity_repository: ActivityRepository = activity_repository
        self.user_repository: UserRepository = user_repository

    def create(self, data: ActivityCreateModel) -> ActivityCreateResponse:
        try:
            user = self.user_repository.find_by_email(data.email)

            activity = Activity(
                type=Type.from_int(data.type),
                name=data.name,
                description=data.description,
                more=data.more,
                start_date=data.start_date,
                end_date=data.end_date,
                place=data.place,
                max_members=data.max_members,
                user=UserSummary(id=user.id, email=user.email),
            )

            self.activity_repository.create(activity)
            self.activity_repository.commit()
        except:
            self.activity_repository.rollback()
            raise

        return ActivityCreateResponse()

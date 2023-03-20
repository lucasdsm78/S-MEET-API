from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse
from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class ActivityCommandUseCase(ABC):
    """ActivityCommandUseCase defines a command usecase inteface related Activity entity."""

    @abstractmethod
    def create(self, email: str, activity_create_model: ActivityCreateModel):
        raise NotImplementedError

    @abstractmethod
    def add_participant(self, activity_id: int, email: str) -> ActivityParticipateResponse:
        raise NotImplementedError

    def delete_participant(self, activity_id: int, email: str) -> ActivityCancelParticipationResponse:
        raise NotImplementedError


class ActivityCommandUseCaseImpl(ActivityCommandUseCase):
    """ActivityCommandUseCaseImpl implements a command usecases related Activity entity."""

    def __init__(
            self,
            activity_repository: ActivityRepository,
            user_repository: UserRepository,
            school_repository: SchoolRepository,
            activity_participant_repository: ActivityParticipantRepository,
    ):
        self.activity_repository: ActivityRepository = activity_repository
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository
        self.activity_participant_repository: ActivityParticipantRepository = activity_participant_repository

    def create(self, email: str, data: ActivityCreateModel) -> ActivityCreateResponse:
        try:
            user = self.user_repository.find_by_email(email)
            school = self.school_repository.find_by_id(data.school_id)

            activity = Activity(
                type=Type.from_str(data.type),
                category=Category.from_str(data.category),
                name=data.name,
                school=school.id,
                description=data.description,
                start_date=data.start_date,
                end_date=data.end_date,
                place=data.place,
                image_activity=data.image_activity,
                max_members=data.max_members,
                user=UserSummary(id=user.id, email=user.email),
            )

            self.activity_repository.create(activity)
            self.activity_repository.commit()
        except:
            self.activity_repository.rollback()
            raise

        return ActivityCreateResponse()

    def add_participant(self, activity_id: int, email: str) -> ActivityParticipateResponse:
        try:
            user = self.user_repository.find_by_email(email)
            activity = self.activity_repository.find_by_id(activity_id)

            activity_participant = ActivityParticipant(
                user_id=user.id,
                activity_id=activity.id
            )

            self.activity_participant_repository.add_participant(activity_participant)
            self.activity_participant_repository.commit()
        except:
            self.activity_participant_repository.rollback()
            raise

        return ActivityParticipateResponse()

    def delete_participant(self, activity_id: int, email: str) -> ActivityCancelParticipationResponse:
        try:
            user = self.user_repository.find_by_email(email)
            activity = self.activity_repository.find_by_id(activity_id)
            activity_participant = self.activity_participant_repository.get_participation(activity.id, user.id)
            self.activity_participant_repository.delete_participant(activity_participant.id)
            self.activity_participant_repository.commit()
        except:
            self.activity_participant_repository.rollback()
            raise

        return ActivityCancelParticipationResponse()

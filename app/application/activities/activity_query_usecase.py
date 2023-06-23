from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from fastapi.responses import FileResponse

from app.application.activities.activity_query_model import ActivityReadModel
from app.domain.activity.exception.activity_exception import ActivityNotFoundError
from app.domain.activity.model.activity import Activity
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.user.repository.user_repository import UserRepository


class ActivityQueryUseCase(ABC):

    @abstractmethod
    def fetch_activities(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_activity_by_id(self, activity_id: int, email: str) -> Optional[ActivityReadModel]:
        raise NotImplementedError

    @abstractmethod
    def check_is_participate(self, activity_id: int, user_id: int) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_image_activity(self, activity_id: int) -> FileResponse:
        raise NotImplementedError


class ActivityQueryUseCaseImpl(ActivityQueryUseCase, BaseModel):
    activity_repository: ActivityRepository
    user_repository: UserRepository
    activity_participant_repository: ActivityParticipantRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_activities(self) -> dict:
        try:
            activities = self.activity_repository.find_activities()
            return dict(
                activities=list(map(lambda activity: ActivityReadModel.from_entity_get_all(
                    activity=activity), activities))
            )

        except Exception as e:
            raise

    def get_activity_by_id(self, activity_id: int, email: str) -> Optional[ActivityReadModel]:
        try:
            activity = self.activity_repository.find_by_id(activity_id)
            if activity is None:
                raise ActivityNotFoundError

            is_participate = self.is_participate(activity.id, email)

        except:
            raise

        return ActivityReadModel.from_entity_get_by_id(activity, is_participate)

    def is_participate(self, activity_id: int, email: str) -> bool:
        try:
            user = self.user_repository.find_by_email(email)
            activity = self.activity_repository.find_by_id(activity_id)
            is_participate = self.activity_participant_repository.find_participation(activity.id, user.id)
            if is_participate is False:
                return False
            return True
        except:
            raise

    def check_is_participate(self, activity_id: int, user_id: int) -> bool:
        try:
            user = self.user_repository.find_by_id(user_id)
            activity = self.activity_repository.find_by_id(activity_id)
            return self.activity_participant_repository.find_participation(activity.id, user.id)
        except:
            raise

    def get_image_activity(self, activity_id: int) -> FileResponse:
        activity = self.activity_repository.find_by_id(activity_id)
        if not activity:
            raise ActivityNotFoundError

        image_path = f"images/activity/{activity.id}/{activity.image_activity}"
        return FileResponse(image_path)
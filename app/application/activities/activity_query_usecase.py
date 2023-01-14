from abc import ABC, abstractmethod
from typing import Optional

from pydantic import BaseModel

from app.application.activities.activity_query_model import ActivityReadModel
from app.domain.activity.exception.activity_exception import ActivityNotFoundError
from app.domain.activity.model.activity import Activity
from app.domain.activity.repository.activity_repository import ActivityRepository


class ActivityQueryUseCase(ABC):

    @abstractmethod
    def fetch_activities(self) -> dict:
        raise NotImplementedError

    @abstractmethod
    def get_activity_by_id(self, activity_id: int) -> Optional[ActivityReadModel]:
        raise NotImplementedError


class ActivityQueryUseCaseImpl(ActivityQueryUseCase, BaseModel):
    activity_repository: ActivityRepository

    class Config:
        arbitrary_types_allowed = True

    def fetch_activities(self) -> dict:
        try:
            activities = self.activity_repository.find_activities()
            return dict(
                activities=list(map(lambda activity: ActivityReadModel.from_entity(
                    activity=activity), activities))
            )

        except Exception as e:
            raise

    def get_activity_by_id(self, activity_id: int) -> Optional[ActivityReadModel]:
        try:
            activity = self.activity_repository.find_by_id(activity_id)
            if activity is None:
                raise ActivityNotFoundError
        except:
            raise

        return ActivityReadModel.from_entity(activity)

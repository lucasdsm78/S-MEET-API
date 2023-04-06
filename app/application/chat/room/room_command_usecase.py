from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse
from app.application.chat.room.room_command_model import RoomCreateModel, RoomCreateResponse, RoomParticipateResponse, \
    RoomCancelParticipationResponse
from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.chat.room.model.room import Room
from app.domain.chat.room.model.room_participant import RoomParticipant
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.school import School
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class RoomCommandUseCase(ABC):
    """RoomCommandUseCase defines a command usecase inteface related Room entity."""

    @abstractmethod
    def create(self, data: RoomCreateModel, school_id: int, user_id: int):
        raise NotImplementedError

    @abstractmethod
    def add_participant_room(self, room_id: int, user_id: int) -> RoomParticipateResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_participant_room(self, room_id: int, user_id: int) -> RoomCancelParticipationResponse:
        raise NotImplementedError


class RoomCommandUseCaseImpl(RoomCommandUseCase):
    """RoomCommandUseCaseImpl implements a command usecases related Room entity."""

    def __init__(
            self,
            room_repository: RoomRepository,
            school_repository: SchoolRepository,
            user_repository: UserRepository,
            room_participant_repository: RoomParticipantRepository,
    ):
        self.room_repository: RoomRepository = room_repository
        self.school_repository: SchoolRepository = school_repository
        self.user_repository: UserRepository = user_repository
        self.room_participant_repository: RoomParticipantRepository = room_participant_repository

    def create(self, data: RoomCreateModel, school_id: int, user_id: int):
        try:
            school = self.school_repository.find_by_id(school_id)

            room = Room(
                name=data.name,
                description=data.description,
                school_id=school.id,
                image_room=data.image_room,
                users=data.users,
            )

            self.add_participant_room(room_id=room.id, user_id=user_id)

            self.room_repository.create(room)
            self.room_repository.commit()
        except:
            self.room_repository.rollback()
            raise

        return RoomCreateResponse()

    def add_participant_room(self, room_id: int, user_id: int) -> RoomParticipateResponse:
        try:
            user = self.user_repository.find_by_id(user_id)

            room = self.room_repository.find_room_by_id(room_id)

            room_participant = RoomParticipant(
                user_id=user.id,
                room_id=room.id
            )

            self.room_participant_repository.add_participant(room_participant)
            self.room_participant_repository.commit()
        except:
            self.room_participant_repository.rollback()
            raise

        return RoomParticipateResponse()

    def delete_participant_room(self, room_id: int, user_id: int) -> RoomCancelParticipationResponse:
        try:
            user = self.user_repository.find_by_id(user_id)
            room = self.room_repository.find_room_by_id(room_id)
            room_participant = self.room_participant_repository.get_participation_room(room.id, user.id)
            self.room_participant_repository.delete_participant_room(room_participant.id)
            self.room_participant_repository.commit()
        except:
            self.room_participant_repository.rollback()
            raise

        return RoomCancelParticipationResponse()
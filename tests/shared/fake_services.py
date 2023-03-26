from typing import Optional, List

from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.email import Email
from app.domain.user.model.password import Password
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from app.domain.user.model.user_summary import UserSummary
from app.domain.user.repository.user_repository import UserRepository


class FakeActivityRepository(ActivityRepository):

    def create(self, activity: Activity) -> Optional[Activity]:
        pass

    def find_activities(self) -> List[Activity]:
        pass

    def find_by_id(self, activity_id: int) -> Optional[Activity]:
        return Activity(
            type=Type.from_str('activity'),
            name='test',
            school=1,
            description='test',
            start_date=10000,
            end_date=100000,
            place='Cergy',
            image_activity='https://www.image.png',
            category=Category.from_str('repas'),
            max_members=50,
            user=UserSummary(Email('test@esieeit.fr'))
        )

    def commit(self):
        pass

    def rollback(self):
        pass


class FakeUserRepository(UserRepository):

    def create(self, user: User) -> Optional[User]:
        pass

    def find_by_email(self, email: str) -> Optional[User]:
        return User(
            email=Email('lucas@esieeit.fr'),
            pseudo='test',
            first_name='test',
            last_name='test',
            school=School(name='esieeit'),
            password=Password('test')
        )

    def find_by_id(self, user_id: int) -> Optional[User]:
        return User(
            email=Email('lucas@esieeit.fr'),
            pseudo='test',
            first_name='test',
            last_name='test',
            school=School(name='esieeit'),
            password=Password('test')
        )

    def find_users(self) -> List[Activity]:
        pass

    def find_users_by_activity(self, activity_id: int) -> List[Activity]:
        pass

    def commit(self):
        pass

    def rollback(self):
        pass


class FakeSchoolRepository(SchoolRepository):

    def create(self, user: User) -> Optional[School]:
        pass

    def find_by_name(self, name: str) -> Optional[School]:
        return School(
            name='esieeit'
        )

    def find_by_id(self, school_id: int) -> Optional[School]:
        return School(
            name='esieeit'
        )

    def commit(self):
        pass

    def rollback(self):
        pass


class FakeActivityParticipantRepository(ActivityParticipantRepository):

    def add_participant(self, activity_participant: ActivityParticipant) -> Optional[ActivityParticipant]:
        pass

    def get_participation(self, activity_id: int, user_id: int) -> Optional[ActivityParticipant]:
        pass

    def find_participation(self, activity_id: int, user_id: int) -> bool:
        pass

    def delete_participant(self, activity_participant_id: int):
        pass

    def commit(self):
        pass

    def rollback(self):
        pass

import copy

from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.user.model.email import Email
from app.domain.user.model.password import Password
from app.domain.user.model.school import School
from app.domain.user.model.user import User
from app.domain.user.model.user_summary import UserSummary


def fake_user() -> User:
    return copy.deepcopy(User(
        email=Email('lucas@esieeit.fr'),
        pseudo='test',
        first_name='test',
        last_name='test',
        school=School(name='esieeit'),
        password=Password('test')
    ))


def fake_school() -> School:
    return copy.deepcopy(School(
        id=1,
        name='esieeit'
    ))


def fake_activity() -> Activity:
    return copy.deepcopy(Activity(
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
    ))


def fake_activity_participant() -> ActivityParticipant:
    return copy.deepcopy(ActivityParticipant(
        user_id=1,
        activity_id=1,
    ))

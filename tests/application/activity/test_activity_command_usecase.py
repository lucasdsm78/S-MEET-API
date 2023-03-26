from unittest.mock import Mock

import pytest

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityCancelParticipationResponse
from app.application.activities.activity_command_usecase import ActivityCommandUseCaseImpl
from tests.shared.fake_datas import fake_user, fake_school, fake_activity, fake_activity_participant
from tests.shared.fake_services import FakeActivityRepository, FakeUserRepository, FakeSchoolRepository, \
    FakeActivityParticipantRepository


class TestActivityCommandUseCase:

    def test_create_activity_return_activity_response_created(self):
        activity_repo = FakeActivityRepository()
        user_repo = FakeUserRepository()
        school_repo = FakeSchoolRepository()
        activity_participant_repo = FakeActivityParticipantRepository()

        user_repo.find_by_email = Mock(return_value=fake_user())
        school_repo.find_by_id = Mock(return_value=fake_school())

        activity_command_usecase = ActivityCommandUseCaseImpl(
            activity_repository=activity_repo,
            user_repository=user_repo,
            school_repository=school_repo,
            activity_participant_repository=activity_participant_repo
        )

        result = activity_command_usecase.create(
            ActivityCreateModel(
                type='activity',
                name='test',
                school_id=1,
                description='test',
                start_date=10000,
                end_date=100000,
                place='Cergy',
                image_activity='https://www.image.png',
                category='repas',
                max_members=50,
            ),
            'test@esieeit.fr'
        )

        assert isinstance(result, ActivityCreateResponse)

    def test_cancel_participation_return_activity_response_cancelled(self):
        activity_repo = FakeActivityRepository()
        user_repo = FakeUserRepository()
        school_repo = FakeSchoolRepository()
        activity_participant_repo = FakeActivityParticipantRepository()

        user_repo.find_by_email = Mock(return_value=fake_user())
        activity_repo.find_by_id = Mock(return_value=fake_activity())
        activity_participant_repo.get_participation = Mock(return_value=fake_activity_participant())

        activity_command_usecase = ActivityCommandUseCaseImpl(
            activity_repository=activity_repo,
            user_repository=user_repo,
            school_repository=school_repo,
            activity_participant_repository=activity_participant_repo
        )

        result = activity_command_usecase.delete_participant(
            1,
            'test@esieeit.fr'
        )

        assert isinstance(result, ActivityCancelParticipationResponse)

from abc import ABC, abstractmethod

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse, ActivityDeleteResponse
from app.application.smeet.smeet_command_model import SmeetCreateResponse, SmeetCreateModel
from app.domain.activity.exception.activity_exception import ActivityNotFoundError
from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.badge.model.badge_summary import BadgeSummary
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.smeet.model.smeet import Smeet
from app.domain.smeet.repository.smeet_repository import SmeetRepository
from app.domain.stats.repository.stat_repository import StatRepository
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class SmeetCommandUseCase(ABC):
    """SmeetCommandUseCase defines a command usecase inteface related Smeet entity."""

    @abstractmethod
    def create(self, user_sender_id: int, user_receiver_id: int, data: SmeetCreateModel) -> SmeetCreateResponse:
        raise NotImplementedError


class SmeetCommandUseCaseImpl(SmeetCommandUseCase):
    """SmeetCommandUseCaseImpl implements a command usecases related Smeet entity."""

    def __init__(
            self,
            smeet_repository: SmeetRepository,
            user_repository: UserRepository,
            stat_repository: StatRepository,
            badge_repository: BadgeRepository
    ):
        self.smeet_repository: SmeetRepository = smeet_repository
        self.user_repository: UserRepository = user_repository
        self.stat_repository: StatRepository = stat_repository
        self.badge_repository: BadgeRepository = badge_repository

    def create(self, user_sender_id: int, user_receiver_id: int, data: SmeetCreateModel) -> SmeetCreateResponse:
        try:
            # Récupération de l'utilisateur connecté
            user_sender = self.user_repository.find_by_id(user_sender_id)

            # Récupération de l'utilisateur qui va recevoir le smeet
            user_receiver = self.user_repository.find_by_id(user_receiver_id)

            smeet = Smeet(
                user_receiver=user_receiver.id,
                user_sender=user_sender.id,
                content=data.content,
                is_edited=data.is_edited
            )

            stat = self.stat_repository.find_by_user_id(user_sender.id)
            stat.smeets_send = stat.smeets_send + 1

            # Enregistrement dans la base de données
            self.smeet_repository.create(smeet)
            self.smeet_repository.commit()
            self.stat_repository.update_stat(stat)
            self.stat_repository.commit()

           # ajouter les routers et ajouter dans les dependency injections

            badge = self.badge_repository.find_by_name('Amoureux fou')

            find_user_badge = self.badge_repository.find_user_badge(badge.id, user_sender.id)
            if not find_user_badge:
                user_badge = UserBadge(
                    badge=badge.id,
                    user=user_sender.id,
                    grade=Grade.from_str('bronze')
                )

                self.badge_repository.add_badge_to_user(user_badge)

            else:
                user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user_sender.id, badge.id)

                if stat.smeets_send == 10:
                    user_badge.grade = Grade.from_str('silver')

                if stat.smeets_send == 50:
                    user_badge.grade = Grade.from_str('gold')

                if stat.smeets_send == 100:
                    user_badge.grade = Grade.from_str('platine')

                self.badge_repository.update_user_badge(user_badge)

            self.badge_repository.commit()
        except:
            self.smeet_repository.rollback()
            self.badge_repository.rollback()
            self.stat_repository.rollback()
            raise

        return SmeetCreateResponse()
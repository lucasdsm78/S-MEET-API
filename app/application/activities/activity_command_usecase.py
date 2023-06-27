import os
import shutil
import shortuuid
from abc import ABC, abstractmethod
from datetime import datetime

from fastapi import UploadFile

from app.application.activities.activity_command_model import ActivityCreateModel, ActivityCreateResponse, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse, ActivityDeleteResponse
from app.domain.activity.exception.activity_exception import ActivityNotFoundError, MaxParticipantsAtteintsError
from app.domain.activity.model.activity import Activity
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.model.category import Category
from app.domain.activity.model.type import Type
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.user.model.email import Email
from app.domain.badge.model.badge_summary import BadgeSummary
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.notification.model.notification import Notification
from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.stats.repository.stat_repository import StatRepository
from app.domain.user.model.user_summary import UserSummary

from app.domain.user.repository.user_repository import UserRepository


class ActivityCommandUseCase(ABC):
    """ActivityCommandUseCase defines a command usecase inteface related Activity entity."""

    @abstractmethod
    def create(self, email: str, activity_create_model: ActivityCreateModel) -> str:
        raise NotImplementedError

    @abstractmethod
    def add_participant(self, activity_id: int, email: str) -> ActivityParticipateResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_participant(self, activity_id: int, email: str) -> ActivityCancelParticipationResponse:
        raise NotImplementedError

    @abstractmethod
    def delete_activity(self, activity_id: int) -> ActivityDeleteResponse:
        raise NotImplementedError


class ActivityCommandUseCaseImpl(ActivityCommandUseCase):
    """ActivityCommandUseCaseImpl implements a command usecases related Activity entity."""

    def __init__(
            self,
            activity_repository: ActivityRepository,
            user_repository: UserRepository,
            school_repository: SchoolRepository,
            activity_participant_repository: ActivityParticipantRepository,
            stat_repository: StatRepository,
            badge_repository: BadgeRepository,
            notification_repository: NotificationRepository
    ):
        self.activity_repository: ActivityRepository = activity_repository
        self.user_repository: UserRepository = user_repository
        self.school_repository: SchoolRepository = school_repository
        self.activity_participant_repository: ActivityParticipantRepository = activity_participant_repository
        self.stat_repository: StatRepository = stat_repository
        self.badge_repository: BadgeRepository = badge_repository
        self.notification_repository: NotificationRepository = notification_repository

    def create(self, email: str, data: ActivityCreateModel) -> str:
        try:
            # Récupération de l'utilisateur connecté
            user = self.user_repository.find_by_email(email)

            # Envoi d'une requête pour savoir si l'école existe bien
            school = self.school_repository.find_by_id(data.school_id)

            uuid = shortuuid.uuid()

            activity = Activity(
                type=Type.from_str(data.type),
                uuid=uuid,
                category=Category.from_str(data.category),
                name=data.name,
                school=school.id,
                description=data.description,
                start_date=data.start_date,
                end_date=data.end_date,
                place=data.place,
                image_activity=f"images/activity/{uuid}/{data.image_activity}",
                max_members=data.max_members,
                user=UserSummary(id=user.id, email=user.email),
            )

            stat = self.stat_repository.find_by_user_id(user.id)
            stat.activities_created = stat.activities_created + 1

            # Enregistrement dans la base de données
            self.activity_repository.create(activity)
            self.activity_repository.commit()
            self.stat_repository.update_stat(stat)
            self.stat_repository.commit()


            badge = self.badge_repository.find_by_name('Organisateur Pro')

            find_user_badge = self.badge_repository.find_user_badge(badge.id, user.id)
            if not find_user_badge:
                grade = Grade.from_str('bronze')
                user_badge = UserBadge(
                    badge=badge.id,
                    user=user.id,
                    grade=grade
                )

                self.badge_repository.add_badge_to_user(user_badge)

                notification = Notification(
                    content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez créé votre première activité",
                    is_read=False,
                    type_notif=TypeNotification.from_str('activity'),
                    user=UserSummary(id=user.id, email=user.email),
                )

                self.notification_repository.create(notification)

            else:
                user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user.id, badge.id)
                print(stat.activities_created)

                if stat.activities_created == 3:
                    grade = Grade.from_str('silver')
                    user_badge.grade = grade
                    notification = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez créé {stat.activities_created} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification)

                if stat.activities_created == 5:
                    grade = Grade.from_str('gold')
                    user_badge.grade = grade
                    notification = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez créé {stat.activities_created} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification)


                if stat.activities_created == 10:
                    grade = Grade.from_str('platine')
                    user_badge.grade = grade
                    notification = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez créé {stat.activities_created} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification)

                self.badge_repository.update_user_badge(user_badge)

            self.badge_repository.commit()
            self.notification_repository.commit()

        except:
            self.activity_repository.rollback()
            self.badge_repository.rollback()
            self.stat_repository.rollback()
            self.notification_repository.rollback()
            raise

        return activity.uuid

    def add_participant(self, activity_id: int, email: str) -> ActivityParticipateResponse:
        try:
            # Récupération du model user de l'utilisateur connecté
            user = self.user_repository.find_by_email(email)

            # Récupération de l'activité choisie par l'utilisateur
            activity = self.activity_repository.find_by_id(activity_id)

            activity_participant = ActivityParticipant(
                user_id=user.id,
                activity_id=activity.id
            )

            current_count_participations = self.activity_participant_repository.count_participations(activity.id)
            if current_count_participations == activity.max_members:
                raise MaxParticipantsAtteintsError

            notification = Notification(
                content=f"L'utilisateur {user.pseudo} a participé à votre activité {activity.name}",
                is_read=False,
                type_notif=TypeNotification.from_str('activity'),
                user=UserSummary(id=activity.user.id, email=activity.user.email),
            )

            self.notification_repository.create(notification)

            stat = self.stat_repository.find_by_user_id(user.id)
            stat.activities_in = stat.activities_in + 1

            # Insertion dans la base de données activity_participants
            self.activity_participant_repository.add_participant(activity_participant)
            self.activity_participant_repository.commit()
            self.stat_repository.update_stat(stat)
            self.stat_repository.commit()

            badge = self.badge_repository.find_by_name('Roi de la fête')

            find_user_badge = self.badge_repository.find_user_badge(badge.id, user.id)
            if not find_user_badge:
                grade = Grade.from_str('bronze')
                user_badge = UserBadge(
                    badge=badge.id,
                    user=user.id,
                    grade=grade
                )

                self.badge_repository.add_badge_to_user(user_badge)
                notification_badge = Notification(
                    content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez participé à votre première activité",
                    is_read=False,
                    type_notif=TypeNotification.from_str('activity'),
                    user=UserSummary(id=user.id, email=user.email),
                )

                self.notification_repository.create(notification_badge)

            else:
                user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user.id, badge.id)

                if stat.activities_in == 5:
                    grade = Grade.from_str('silver')
                    user_badge.grade = grade
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez participé à {stat.activities_in} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

                if stat.activities_in == 20:
                    grade = Grade.from_str('gold')
                    user_badge.grade = grade
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez participé à {stat.activities_in} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

                if stat.activities_in == 50:
                    grade = Grade.from_str('platine')
                    user_badge.grade = grade
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez participé à {stat.activities_in} activités",
                        is_read=False,
                        type_notif=TypeNotification.from_str('activity'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

                self.badge_repository.update_user_badge(user_badge)

            self.badge_repository.commit()
            self.notification_repository.commit()
        except:
            self.activity_participant_repository.rollback()
            self.badge_repository.rollback()
            self.stat_repository.rollback()
            self.notification_repository.rollback()
            raise

        return ActivityParticipateResponse()

    def delete_participant(self, activity_id: int, email: str) -> ActivityCancelParticipationResponse:
        try:
            user = self.user_repository.find_by_email(email)
            activity = self.activity_repository.find_by_id(activity_id)
            activity_participant = self.activity_participant_repository.get_participation(activity.id, user.id)
            self.activity_participant_repository.delete_participant(activity_participant.id)
            self.activity_participant_repository.commit()


            notification = Notification(
                content=f"L'utilisateur {user.pseudo} a quitté votre activité {activity.name}",
                is_read=False,
                type_notif=TypeNotification.from_str('activity'),
                user=UserSummary(id=activity.user.id, email=activity.user.email),
            )

            self.notification_repository.create(notification)
            self.notification_repository.commit()
        except:
            self.activity_participant_repository.rollback()
            self.notification_repository.rollback()
            raise

        return ActivityCancelParticipationResponse()

    def delete_activity(self, activity_id: int) -> ActivityDeleteResponse:
        try:
            existing_activity = self.activity_repository.find_by_id(activity_id)
            if existing_activity is None:
                raise ActivityNotFoundError

            self.activity_repository.delete_activity(activity_id)
            self.activity_repository.commit()
        except:
            self.activity_repository.rollback()
            raise

        return ActivityDeleteResponse()

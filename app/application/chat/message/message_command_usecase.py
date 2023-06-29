from abc import ABC, abstractmethod
from app.application.chat.message.message_command_model import MessageCreateModel, MessageCreateResponse
from app.domain.badge.model.properties.grade import Grade
from app.domain.badge.model.properties.user_badge import UserBadge
from app.domain.badge.repository.badge_repository import BadgeRepository
from app.domain.chat.message.model.message import Message
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.notification.model.notification import Notification
from app.domain.notification.model.properties.type_notif import TypeNotification
from app.domain.notification.repository.notification_repository import NotificationRepository
from app.domain.stats.repository.stat_repository import StatRepository
from app.domain.user.model.user_summary import UserSummary
from app.domain.user.repository.user_repository import UserRepository


class MessageCommandUseCase(ABC):
    """MessageCommandUseCase defines a command usecase inteface related Message entity."""

    @abstractmethod
    def create(self, data: MessageCreateModel, user_id: int):
        raise NotImplementedError


class MessageCommandUseCaseImpl(MessageCommandUseCase):
    """MessageCommandUseCaseImpl implements a command usecases related Message entity."""

    def __init__(
            self,
            message_repository: MessageRepository,
            user_repository: UserRepository,
            room_repository: RoomRepository,
            stat_repository: StatRepository,
            badge_repository: BadgeRepository,
            notification_repository: NotificationRepository,
            room_participant_repository: RoomParticipantRepository
    ):
        self.message_repository: MessageRepository = message_repository
        self.user_repository: UserRepository = user_repository
        self.room_repository: RoomRepository = room_repository
        self.stat_repository: StatRepository = stat_repository
        self.badge_repository: BadgeRepository = badge_repository
        self.room_participant_repository: RoomParticipantRepository = room_participant_repository
        self.notification_repository: NotificationRepository = notification_repository

    def create(self, data: MessageCreateModel, user_id: int):
        try:
            user = self.user_repository.find_by_id(user_id)
            room = self.room_repository.find_room_by_id(room_id=data.room_id)

            message = Message(
                content=data.content,
                room_id=room.id,
                user_id=user.id
            )

            stat = self.stat_repository.find_by_user_id(user.id)
            stat.messages_send = stat.messages_send + 1

            users = self.room_participant_repository.find_participants_by_room(room.id)

            for user_room in users:
                notification = Notification(
                    content=f"{user.pseudo} a envoyé un message : {data.content} dans le chat {room.name}",
                    is_read=False,
                    type_notif=TypeNotification.from_str('message'),
                    user=UserSummary(id=user_room.id, email=user_room.email),
                )
                self.notification_repository.create(notification)



            self.message_repository.create(message)
            self.message_repository.commit()
            self.stat_repository.update_stat(stat)
            self.stat_repository.commit()
            self.notification_repository.commit()

            badge = self.badge_repository.find_by_name('Messager')

            if stat.messages_send == 10:
                grade = Grade.from_str('bronze')
                user_badge = UserBadge(
                    badge=badge.id,
                    user=user.id,
                    grade=grade
                )

                self.badge_repository.add_badge_to_user(user_badge)
                notification_badge = Notification(
                    content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez envoyé {stat.messages_send} messages",
                    is_read=False,
                    type_notif=TypeNotification.from_str('message'),
                    user=UserSummary(id=user.id, email=user.email),
                )

                self.notification_repository.create(notification_badge)

            else:
                if stat.messages_send == 20:
                    user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user.id, badge.id)
                    grade = Grade.from_str('silver')
                    user_badge.grade = grade
                    self.badge_repository.update_user_badge(user_badge)
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez envoyé {stat.messages_send} messages",
                        is_read=False,
                        type_notif=TypeNotification.from_str('message'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

                if stat.messages_send == 50:
                    user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user.id, badge.id)
                    grade = Grade.from_str('gold')
                    user_badge.grade = grade
                    self.badge_repository.update_user_badge(user_badge)
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez envoyé {stat.messages_send} messages",
                        is_read=False,
                        type_notif=TypeNotification.from_str('message'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

                if stat.messages_send == 100:
                    user_badge = self.badge_repository.find_user_badge_by_user_id_badge_id(user.id, badge.id)
                    grade = Grade.from_str('platine')
                    user_badge.grade = grade
                    self.badge_repository.update_user_badge(user_badge)
                    notification_badge = Notification(
                        content=f"Vous avez obtenu le badge {badge.name} avec le grade {grade.value} car vous avez envoyé {stat.messages_send} messages",
                        is_read=False,
                        type_notif=TypeNotification.from_str('message'),
                        user=UserSummary(id=user.id, email=user.email),
                    )

                    self.notification_repository.create(notification_badge)

            self.badge_repository.commit()
            self.notification_repository.commit()
        except:
            self.message_repository.rollback()
            self.badge_repository.rollback()
            self.stat_repository.rollback()
            self.notification_repository.rollback()
            raise

        return MessageCreateResponse()
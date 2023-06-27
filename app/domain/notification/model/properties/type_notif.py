from enum import Enum
from dataclasses import dataclass

from app.domain.badge.exception.badge_exception import InvalidGradeException
from app.domain.notification.exception.notification_exception import InvalidTypeNotifException


@dataclass(init=False, eq=True, frozen=True)
class TypeNotification(Enum):
    event = 'event'
    activity = 'activity'
    badge = 'badge'
    smeet = 'smeet'
    quiz = 'quiz'
    beta = 'beta'

    @classmethod
    def from_str(cls, type_notif: str) -> "TypeNotification":
        try:
            return cls(type_notif)
        except ValueError:
            raise InvalidTypeNotifException(type_notif) from None
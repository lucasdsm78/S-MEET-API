from enum import Enum
from dataclasses import dataclass

from app.domain.activity.exception.activity_exception import InvalidTypeException


@dataclass(init=False, eq=True, frozen=True)
class Type(Enum):
    activity = 'activity'
    event = 'event'

    @classmethod
    def from_str(cls, type: str) -> "Type":
        try:
            return cls(type)
        except ValueError:
            raise InvalidTypeException(type) from None

    def is_event(self) -> bool:
        return self.value == Type.event.value

    def is_activity(self) -> bool:
        return self.value == self.activity.value
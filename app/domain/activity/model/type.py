from enum import Enum
from dataclasses import dataclass

from app.domain.activity.exception.activity_exception import InvalidTypeException


@dataclass(init=False, eq=True, frozen=True)
class Type(Enum):
    activity = 1
    event = 2

    @classmethod
    def from_int(cls, type: int) -> "Type":
        try:
            return cls(type)
        except ValueError:
            raise InvalidTypeException(type) from None

    def to_int(self) -> int:
        return int(self.value.__str__())

    def is_event(self) -> bool:
        return self.value == Type.event.value

    def is_activity(self) -> bool:
        return self.value == self.activity.value
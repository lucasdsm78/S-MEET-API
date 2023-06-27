from enum import Enum
from dataclasses import dataclass

from app.domain.badge.exception.badge_exception import InvalidGradeException


@dataclass(init=False, eq=True, frozen=True)
class Grade(Enum):
    bronze = 'bronze'
    silver = 'silver'
    gold = 'gold'
    platine = 'platine'

    @classmethod
    def from_str(cls, grade: str) -> "Grade":
        try:
            return cls(grade)
        except ValueError:
            raise InvalidGradeException(grade) from None
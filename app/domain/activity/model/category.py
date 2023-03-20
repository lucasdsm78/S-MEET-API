from enum import Enum
from dataclasses import dataclass

from app.domain.activity.exception.activity_exception import InvalidCategoryException


@dataclass(init=False, eq=True, frozen=True)
class Category(Enum):
    repas = 'repas'
    soiree = 'soiree'
    voyage = 'voyage'
    pause = 'pause'
    after_work = 'after_work'

    @classmethod
    def from_str(cls, category: str) -> "Category":
        try:
            return cls(category)
        except ValueError:
            raise InvalidCategoryException(category) from None

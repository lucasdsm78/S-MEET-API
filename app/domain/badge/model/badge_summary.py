from typing import Optional

from app.domain.user.model.email import Email


class BadgeSummary:

    def __init__(
            self,
            name: str,
            description: str,
            id: Optional[int] = None
    ):
        self.id: int = id
        self.name: str = name
        self.description: str = description

    def __eq__(self, o: object) -> bool:
        if isinstance(o, BadgeSummary):
            return self.id == o.id

        return False
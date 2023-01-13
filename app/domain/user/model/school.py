from typing import Optional

from pydantic import BaseModel


class School:
    def __init__(
            self,
            name: str,
            id: Optional[int] = None
    ):
        self.id: int = id
        self.name: str = name

    class Config():
        orm_mode = True

from typing import Optional

from pydantic import BaseModel


class School(BaseModel):
    id: Optional[int] = None
    name: str

    class Config():
        orm_mode = True

    @classmethod
    def create(cls, name: str):
        return cls(name=name)

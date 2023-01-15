from typing import Union, Optional

from sqlalchemy import Column, String, Integer, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.domain.user.model.school import School
from app.infrastructure.sqlite.database import Base


class DBSchool(Base):
    __tablename__ = "school"
    id: Union[int, Column] = Column(Integer, primary_key=True, autoincrement=True)
    name: Union[str, Column] = Column(String, nullable=False)
    user = relationship("DBUser", back_populates="school")

    def to_entity(self) -> School:
        return School(
            name=self.name
        )

    @staticmethod
    def from_entity(school: School, db_school: Optional["DBSchool"] = None) -> "DBSchool":
        to_update = db_school if db_school is not None else DBSchool()
        to_update.name = school.name

        return to_update

from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.model.school import School
from app.infrastructure.sqlite.school.db_school import DBSchool


class SchoolRepositoryImpl(SchoolRepository):
    """UserRepositoryImpl implements CRUD operations related User entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_by_name(self, name: str) -> Optional[School]:
        try:
            school_db = self.session.query(DBSchool).filter_by(name=name).one()
        except NoResultFound:
            return None
        except:
            raise

        return school_db.to_entity()

    def find_by_id(self, school_id: int) -> Optional[School]:
        try:
            school_db = self.session.query(DBSchool).filter_by(id=school_id).one()
        except NoResultFound:
            return None
        except:
            raise

        return school_db.to_entity()

    def create(self, school: School):
        school_db = DBSchool.from_entity(school)
        try:
            self.session.add(school_db)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
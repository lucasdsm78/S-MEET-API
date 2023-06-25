from typing import List

from sqlalchemy.orm.session import Session
from app.domain.smeet.model.smeet import Smeet
from app.domain.smeet.repository.smeet_repository import SmeetRepository
from app.infrastructure.sqlite.smeet.db_smeet import DBSmeet


class SmeetRepositoryImpl(SmeetRepository):
    """SmeetRepositoryImpl implements CRUD operations related Smeet entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session


    def create(self, smeet: Smeet):
        smeet_db = DBSmeet.from_entity(smeet)
        try:
            self.session.add(smeet_db)
        except:
            raise

    def find_smeets(self) -> List[Smeet]:
        try:
            smeet_dbs = (
                self.session.query(DBSmeet)
                .order_by(DBSmeet.created_at)
                .all()
            )
        except:
            raise

        if len(smeet_dbs) == 0:
            return []

        return list(map(lambda smeet_db: smeet_db.to_entity(), smeet_dbs))


    def find_smeets_by_user_receiver_id(self, user_receiver_id: int) -> List[Smeet]:
        try:
            smeet_dbs = (
                self.session.query(DBSmeet)
                .filter_by(user_receiver_id=user_receiver_id)
                .order_by(DBSmeet.created_at)
                .all()
            )
        except:
            raise

        if len(smeet_dbs) == 0:
            return []

        return list(map(lambda smeet_db: smeet_db.to_entity(), smeet_dbs))


    def find_smeets_by_user_sender_id(self, user_sender_id: int) -> List[Smeet]:
        try:
            smeet_dbs = (
                self.session.query(DBSmeet)
                .filter_by(user_sender_id=user_sender_id)
                .order_by(DBSmeet.created_at)
                .all()
            )
        except:
            raise

        if len(smeet_dbs) == 0:
            return []

        return list(map(lambda smeet_db: smeet_db.to_entity(), smeet_dbs))

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
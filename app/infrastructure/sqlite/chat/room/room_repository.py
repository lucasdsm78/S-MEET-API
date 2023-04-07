from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.chat.room.exception.room_exception import RoomNotFoundError
from app.domain.chat.room.model.room import Room
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.infrastructure.sqlite.chat.room.db_room import DBRoom


class RoomRepositoryImpl(RoomRepository):
    """RoomRepositoryImpl implements CRUD operations related Room entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def find_room_by_id(self, room_id: int) -> Optional[Room]:
        try:
            room_db = self.session.query(DBRoom).filter_by(id=room_id).one()
        except NoResultFound:
            raise RoomNotFoundError
        except Exception:
            raise

        return room_db.to_entity()

    def create(self, room: Room):
        room_db = DBRoom.from_entity(room)
        try:
            self.session.add(room_db)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
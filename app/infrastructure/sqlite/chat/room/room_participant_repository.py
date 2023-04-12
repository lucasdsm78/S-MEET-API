from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.chat.room.exception.room_exception import RoomNotFoundError, RoomParticipantNotFoundError
from app.domain.chat.room.model.room import Room
from app.domain.chat.room.model.room_participant import RoomParticipant
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.user.model.user import User
from app.infrastructure.sqlite.chat.room.db_room import DBRoom
from app.infrastructure.sqlite.chat.room.db_room_participant import DBRoomParticipants
from app.infrastructure.sqlite.user.db_user import DBUser


class RoomParticipantRepositoryImpl(RoomParticipantRepository):
    """RoomParticipantRepositoryImpl implements CRUD operations related RoomParticipant entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def add_participant(self, room_participant: RoomParticipant):
        room_participant_db = DBRoomParticipants.from_entity(room_participant)
        try:
            self.session.add(room_participant_db)
        except:
            raise

    def delete_participant_room(self, room_participant_id: int):
        try:
            self.session.query(DBRoomParticipants).filter_by(id=room_participant_id).delete()
        except:
            raise

    def find_conversations_by_user(self, user_id: int) -> List[Room]:
        try:
            rooms_dbs = (
                self.session.query(DBRoom)
                .join(DBRoomParticipants)
                .filter(DBRoom.id == DBRoomParticipants.room_id)
                .join(DBUser)
                .filter(DBRoomParticipants.user_id == DBUser.id)
                .filter(DBRoomParticipants.user_id == user_id)
                .order_by(DBRoom.created_at)
                .all()
            )
        except:
            raise

        if len(rooms_dbs) == 0:
            return []

        return list(map(lambda room_db: room_db.to_entity(), rooms_dbs))

    def find_participants_by_room(self, room_id: int) -> List[User]:
        try:
            users_dbs = (
                self.session.query(DBUser)
                .join(DBRoomParticipants)
                .filter(DBUser.id == DBRoomParticipants.user_id)
                .join(DBRoom)
                .filter(DBRoomParticipants.room_id == DBRoom.id)
                .filter(DBRoomParticipants.room_id == room_id)
                .all()
            )
        except:
            raise

        if len(users_dbs) == 0:
            return []

        return list(map(lambda user_db: user_db.to_entity(), users_dbs))

    def get_participation_room(self, room_id: int, user_id: int) -> Optional[RoomParticipant]:
        try:
            room_participant_db = self.session.query(DBRoomParticipants).filter_by(
                room_id=room_id,
                user_id=user_id
            ).one()
        except NoResultFound:
            raise RoomParticipantNotFoundError
        except Exception:
            raise

        return room_participant_db.to_entity()

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
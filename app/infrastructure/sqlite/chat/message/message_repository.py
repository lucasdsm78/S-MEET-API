from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.chat.message.exception.message_exception import MessageNotFoundError
from app.domain.chat.message.model.message import Message
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.infrastructure.sqlite.chat.message.db_message import DBMessage
from app.infrastructure.sqlite.chat.room.db_room import DBRoom


class MessageRepositoryImpl(MessageRepository):
    """MessageRepositoryImpl implements CRUD operations related Message entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def create(self, message: Message):
        message_db = DBMessage.from_entity(message)
        try:
            self.session.add(message_db)
        except:
            raise

    def find_messages_by_room(self, room_id: int) -> List[Message]:
        try:
            messages_dbs = (
                self.session.query(DBMessage)
                .join(DBRoom)
                .filter(DBRoom.id == room_id)
                .order_by(DBMessage.created_at)
                .all()
            )
        except:
            raise

        if len(messages_dbs) == 0:
            return []

        return list(map(lambda message_db: message_db.to_entity(), messages_dbs))

    def last(self, room_id: int) -> Optional[Message]:
        try:
            last_message_db = self.session.query(DBMessage).filter_by(room_id=room_id).order_by(DBMessage.id.desc()).first()
        except NoResultFound:
            raise MessageNotFoundError
        except Exception:
            raise

        return last_message_db.to_entity()

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()

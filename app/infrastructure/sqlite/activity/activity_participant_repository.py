from sqlalchemy.orm.session import Session

from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.infrastructure.sqlite.activity.db_activity_participants import DBActivityParticipants


class ActivityParticipantRepositoryImpl(ActivityParticipantRepository):
    """ActivityParticipantRepositoryImpl implements CRUD operations related ActivityParticipant
     entity using SQLAlchemy."""

    def __init__(self, session: Session):
        self.session: Session = session

    def add_participant(self, activity_participant: ActivityParticipant):
        activity_participant_db = DBActivityParticipants.from_entity(activity_participant)
        try:
            self.session.add(activity_participant_db)
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
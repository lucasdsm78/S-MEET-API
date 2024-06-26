from typing import Optional, List

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm.session import Session

from app.domain.activity.exception.activity_exception import ActivityParticipantNotFoundError
from app.domain.activity.model.activity_participants import ActivityParticipant
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.infrastructure.sqlite.activity.db_activity import DBActivity
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

    def get_participation(self, activity_id: int, user_id: int) -> Optional[ActivityParticipant]:
        try:
            activity_participant_db = self.session.query(DBActivityParticipants).filter_by(
                activity_id=activity_id,
                user_id=user_id
            ).one()
        except NoResultFound:
            raise ActivityParticipantNotFoundError
        except Exception:
            raise

        return activity_participant_db.to_entity()

    def find_participation(self, activity_id: int, user_id: int) -> bool:
        try:
            result = False
            activity_participant_db = self.session.query(DBActivityParticipants).filter_by(
                activity_id=activity_id,
                user_id=user_id
            ).count()

            if activity_participant_db != 0:
                result = True
        except Exception:
            raise

        return result

    def find_participants_by_activity_id(self, activity_id: int) -> List[ActivityParticipant]:
        try:
            participants_dbs = (
                self.session.query(DBActivityParticipants)
                .join(DBActivity)
                .filter(DBActivity.id == activity_id)
                .all()
            )
        except:
            raise

        if len(participants_dbs) == 0:
            return []

        return list(map(lambda participant_db: participant_db.to_entity(), participants_dbs))

    def count_participations(self, activity_id: int) -> int:
        try:
            count = self.session.query(DBActivityParticipants).filter_by(
                activity_id=activity_id
            ).count()
        except Exception:
            raise

        return count

    def delete_participant(self, activity_participant_id: int):
        try:
            self.session.query(DBActivityParticipants).filter_by(id=activity_participant_id).delete()
        except:
            raise

    def begin(self):
        self.session.begin()

    def commit(self):
        self.session.commit()

    def rollback(self):
        self.session.rollback()
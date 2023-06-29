from app.application.activities.activity_command_usecase import ActivityCommandUseCase, ActivityCommandUseCaseImpl
from app.application.activities.activity_query_usecase import ActivityQueryUseCase, ActivityQueryUseCaseImpl
from app.application.chat.message.message_command_usecase import MessageCommandUseCase, MessageCommandUseCaseImpl
from app.application.chat.message.message_query_usecase import MessageQueryUseCase, MessageQueryUseCaseImpl
from app.application.chat.room.room_command_usecase import RoomCommandUseCase, RoomCommandUseCaseImpl
from app.application.chat.room.room_query_usecase import RoomQueryUseCase, RoomQueryUseCaseImpl
from app.application.friend.friend_command_usecase import FriendCommandUseCase, FriendCommandUseCaseImpl
from app.application.friend.friend_query_usecase import FriendQueryUseCaseImpl, FriendQueryUseCase
from app.application.quiz.quiz_command_usecase import QuizCommandUseCase, QuizCommandUseCaseImpl
from app.application.quiz.quiz_query_usecase import QuizQueryUseCase, QuizQueryUseCaseImpl
from app.application.school.school_command_usecase import SchoolCommandUseCase, SchoolCommandUseCaseImpl
from app.application.user.bio.user_bio_command_usecase import UserBioCommandUseCase, UserBioCommandUseCaseImpl
from app.application.user.bio.user_bio_query_usecase import UserBioQueryUseCase, UserBioQueryUseCaseImpl
from app.application.user.user_command_usecase import UserCommandUseCase, UserCommandUseCaseImpl
from app.application.user.user_query_usecase import UserQueryUseCase, UserQueryUseCaseImpl
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.chat.message.repository.message_repository import MessageRepository
from app.domain.chat.room.repository.room_participant_repository import RoomParticipantRepository
from app.domain.chat.room.repository.room_repository import RoomRepository
from app.domain.friend.repository.friend_repository import FriendRepository
from app.domain.quiz.repository.quiz_repository import QuizRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.services.file_uploader.file_uploader import FileUploader
from app.domain.services.hash import Hash
from app.domain.services.manager_token import ManagerToken
from app.domain.services.socket_manager.socket_manager import SocketManager
from app.domain.user.bio.repository.user_bio_repository import UserBioRepository
from app.domain.user.repository.user_repository import UserRepository
from app.infrastructure.config import Settings

from functools import lru_cache
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.infrastructure.services.authentication import AuthenticationToken
from app.infrastructure.services.file_uploader.file_uploader import FileUploaderImpl
from app.infrastructure.services.hash import HashImpl
from app.infrastructure.services.jwt_bearer import JwtBearer
from app.infrastructure.services.manager_token import JwtManagerTokenImpl
from app.infrastructure.services.socket_manager.socket_manager import SocketManagerImpl
from app.infrastructure.sqlite.activity.activity_participant_repository import ActivityParticipantRepositoryImpl
from app.infrastructure.sqlite.activity.activity_repository import ActivityRepositoryImpl
from app.infrastructure.sqlite.chat.message.message_repository import MessageRepositoryImpl
from app.infrastructure.sqlite.chat.room.room_participant_repository import RoomParticipantRepositoryImpl
from app.infrastructure.sqlite.chat.room.room_repository import RoomRepositoryImpl
from app.infrastructure.sqlite.database import create_tables, SessionLocal
from app.infrastructure.sqlite.friend.friend_repository import FriendRepositoryImpl
from app.infrastructure.sqlite.quiz.quiz_repository import QuizRepositoryImpl
from app.infrastructure.sqlite.school.school_repository import SchoolRepositoryImpl
from app.infrastructure.sqlite.user.bio.user_bio_repository import UserBioRepositoryImpl
from app.infrastructure.sqlite.user.user_repository import UserRepositoryImpl

# create database
create_tables()

jwt_auth = JwtBearer()


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def socket_manager_dependency() -> SocketManager:
    return SocketManagerImpl()


def file_uploader_dependency() -> FileUploader:
    return FileUploaderImpl()


def manager_token_dependency(settings: Settings = Depends(get_settings)) -> ManagerToken:
    return JwtManagerTokenImpl(settings=settings)


def hash_dependency() -> Hash:
    return HashImpl()


def user_repository_dependency(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepositoryImpl(session)


def user_bio_repository_dependency(session: Session = Depends(get_session)) -> UserBioRepositoryImpl:
    return UserBioRepositoryImpl(session)


def school_repository_dependency(session: Session = Depends(get_session)) -> SchoolRepository:
    return SchoolRepositoryImpl(session)


def activity_repository_dependency(session: Session = Depends(get_session)) -> ActivityRepository:
    return ActivityRepositoryImpl(session)


def friend_repository_dependency(session: Session = Depends(get_session)) -> FriendRepository:
    return FriendRepositoryImpl(session)


def quiz_repository_dependency(session: Session = Depends(get_session)) -> QuizRepository:
    return QuizRepositoryImpl(session)


def activity_participant_repository_dependency(session: Session = Depends(get_session)) \
        -> ActivityParticipantRepository:
    return ActivityParticipantRepositoryImpl(session)


def room_repository_dependency(session: Session = Depends(get_session)) -> RoomRepository:
    return RoomRepositoryImpl(session)


def message_repository_dependency(session: Session = Depends(get_session)) -> MessageRepository:
    return MessageRepositoryImpl(session)


def room_participant_repository_dependency(session: Session = Depends(get_session)) -> RoomParticipantRepository:
    return RoomParticipantRepositoryImpl(session)


def user_command_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency),
        school_repository: SchoolRepository = Depends(school_repository_dependency),
        user_bio_repository: UserBioRepository = Depends(user_bio_repository_dependency),
        hasher: Hash = Depends(hash_dependency),
        manager_token: ManagerToken = Depends(manager_token_dependency)
) -> UserCommandUseCase:
    return UserCommandUseCaseImpl(
        user_repository=user_repository,
        school_repository=school_repository,
        user_bio_repository=user_bio_repository,
        hasher=hasher,
        manager_token=manager_token
    )


def user_bio_command_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency),
        user_bio_repository: UserBioRepository = Depends(user_bio_repository_dependency)
) -> UserBioCommandUseCase:
    return UserBioCommandUseCaseImpl(
        user_repository=user_repository,
        user_bio_repository=user_bio_repository
    )


def user_query_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency)
) -> UserQueryUseCase:
    return UserQueryUseCaseImpl(
        user_repository=user_repository
    )


def user_bio_query_usecase(
        user_bio_repository: UserBioRepository = Depends(user_bio_repository_dependency)
) -> UserBioQueryUseCase:
    return UserBioQueryUseCaseImpl(
        user_bio_repository=user_bio_repository
    )


def school_command_usecase(
        school_repository: SchoolRepository = Depends(school_repository_dependency)
) -> SchoolCommandUseCase:
    return SchoolCommandUseCaseImpl(
        school_repository=school_repository
    )


def activity_command_usecase(
        activity_repository: ActivityRepository = Depends(activity_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
        school_repository: SchoolRepository = Depends(school_repository_dependency),
        activity_participant_repository: ActivityParticipantRepository =
        Depends(activity_participant_repository_dependency),
) -> ActivityCommandUseCase:
    return ActivityCommandUseCaseImpl(
        activity_repository=activity_repository,
        user_repository=user_repository,
        school_repository=school_repository,
        activity_participant_repository=activity_participant_repository,
    )


def activity_query_usecase(
        activity_repository: ActivityRepository = Depends(activity_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
        activity_participant_repository: ActivityParticipantRepository =
        Depends(activity_participant_repository_dependency),
) -> ActivityQueryUseCase:
    return ActivityQueryUseCaseImpl(
        activity_repository=activity_repository,
        user_repository=user_repository,
        activity_participant_repository=activity_participant_repository
    )


def quiz_command_usecase(
        quiz_repository: QuizRepository = Depends(quiz_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
) -> QuizCommandUseCase:
    return QuizCommandUseCaseImpl(
        quiz_repository=quiz_repository,
        user_repository=user_repository
    )


def quiz_query_usecase(
        quiz_repository: QuizRepository = Depends(quiz_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
) -> QuizQueryUseCase:
    return QuizQueryUseCaseImpl(
        quiz_repository=quiz_repository,
        user_repository=user_repository
    )


def room_query_usecase(
        room_repository: RoomRepository = Depends(room_repository_dependency),
        room_participant_repository: RoomParticipantRepository =
        Depends(room_participant_repository_dependency),
) -> RoomQueryUseCase:
    return RoomQueryUseCaseImpl(
        room_repository=room_repository,
        room_participant_repository=room_participant_repository
    )


def room_command_usecase(
        room_repository: RoomRepository = Depends(room_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
        school_repository: SchoolRepository = Depends(school_repository_dependency),
        room_participant_repository: RoomParticipantRepository =
        Depends(room_participant_repository_dependency),
) -> RoomCommandUseCase:
    return RoomCommandUseCaseImpl(
        room_repository=room_repository,
        school_repository=school_repository,
        user_repository=user_repository,
        room_participant_repository=room_participant_repository
    )


def friend_command_usecase(
        friend_repository: FriendRepository = Depends(friend_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
) -> FriendCommandUseCase:
    return FriendCommandUseCaseImpl(
        friend_repository=friend_repository,
        user_repository=user_repository
    )


def friend_query_usecase(
        friend_repository: FriendRepository = Depends(friend_repository_dependency),
) -> FriendQueryUseCase:
    return FriendQueryUseCaseImpl(
        friend_repository=friend_repository
    )


def message_command_usecase(
        message_repository: MessageRepository = Depends(message_repository_dependency),
        user_repository: UserRepository = Depends(user_repository_dependency),
        room_repository: RoomRepository = Depends(room_repository_dependency),
) -> MessageCommandUseCase:
    return MessageCommandUseCaseImpl(
        message_repository=message_repository,
        user_repository=user_repository,
        room_repository=room_repository
    )


def message_query_usecase(
        room_repository: RoomRepository = Depends(room_repository_dependency),
        message_repository: MessageRepository = Depends(message_repository_dependency),
) -> MessageQueryUseCase:
    return MessageQueryUseCaseImpl(
        room_repository=room_repository,
        message_repository=message_repository
    )


def authentication(
        manager_token: ManagerToken = Depends(manager_token_dependency),
        token: str = Depends(jwt_auth)
) -> str:
    token_authenticator = AuthenticationToken(
        manager_token=manager_token,
        token=token
    )
    return token_authenticator.authentication()


def current_user(token: str = Depends(authentication),
                 manager_token: ManagerToken = Depends(manager_token_dependency)
                 ) -> dict:
    return manager_token.decode_token_login(token)

from fastapi.security import HTTPBearer

from app.application.activities.activity_command_usecase import ActivityCommandUseCase, ActivityCommandUseCaseImpl
from app.application.activities.activity_query_usecase import ActivityQueryUseCase, ActivityQueryUseCaseImpl
from app.application.school.school_command_usecase import SchoolCommandUseCase, SchoolCommandUseCaseImpl
from app.application.user.user_command_usecase import UserCommandUseCase, UserCommandUseCaseImpl
from app.application.user.user_query_usecase import UserQueryUseCase, UserQueryUseCaseImpl
from app.domain.activity.repository.activity_participant_repository import ActivityParticipantRepository
from app.domain.activity.repository.activity_repository import ActivityRepository
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.services.hash import Hash
from app.domain.services.manager_token import ManagerToken
from app.domain.user.repository.user_repository import UserRepository
from app.infrastructure.config import Settings

from functools import lru_cache
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.infrastructure.services.authentication import AuthenticationToken
from app.infrastructure.services.hash import HashImpl
from app.infrastructure.services.jwt_bearer import JwtBearer
from app.infrastructure.services.manager_token import JwtManagerTokenImpl
from app.infrastructure.sqlite.activity.activity_participant_repository import ActivityParticipantRepositoryImpl
from app.infrastructure.sqlite.activity.activity_repository import ActivityRepositoryImpl
from app.infrastructure.sqlite.database import create_tables, SessionLocal
from app.infrastructure.sqlite.school.school_repository import SchoolRepositoryImpl
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


def manager_token_dependency(settings: Settings = Depends(get_settings)) -> ManagerToken:
    return JwtManagerTokenImpl(settings=settings)


def hash_dependency() -> Hash:
    return HashImpl()


def user_repository_dependency(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepositoryImpl(session)


def school_repository_dependency(session: Session = Depends(get_session)) -> SchoolRepository:
    return SchoolRepositoryImpl(session)


def activity_repository_dependency(session: Session = Depends(get_session)) -> ActivityRepository:
    return ActivityRepositoryImpl(session)


def activity_participant_repository_dependency(session: Session = Depends(get_session)) \
        -> ActivityParticipantRepository:
    return ActivityParticipantRepositoryImpl(session)


def user_command_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency),
        school_repository: SchoolRepository = Depends(school_repository_dependency),
        hasher: Hash = Depends(hash_dependency),
        manager_token: ManagerToken = Depends(manager_token_dependency)
) -> UserCommandUseCase:
    return UserCommandUseCaseImpl(
        user_repository=user_repository,
        school_repository=school_repository,
        hasher=hasher,
        manager_token=manager_token
    )


def user_query_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency)
) -> UserQueryUseCase:
    return UserQueryUseCaseImpl(
        user_repository=user_repository
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
        activity_participant_repository: ActivityParticipantRepository =
        Depends(activity_participant_repository_dependency),
) -> ActivityCommandUseCase:
    return ActivityCommandUseCaseImpl(
        activity_repository=activity_repository,
        user_repository=user_repository,
        activity_participant_repository=activity_participant_repository,
    )


def activity_query_usecase(
        activity_repository: ActivityRepository = Depends(activity_repository_dependency)
) -> ActivityQueryUseCase:
    return ActivityQueryUseCaseImpl(
        activity_repository=activity_repository
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

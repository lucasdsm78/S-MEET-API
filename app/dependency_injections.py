from app.application.school.school_command_usecase import SchoolCommandUseCase, SchoolCommandUseCaseImpl
from app.application.user.user_command_usecase import UserCommandUseCase, UserCommandUseCaseImpl
from app.domain.school.repository.school_repository import SchoolRepository
from app.domain.user.repository.user_repository import UserRepository
from app.infrastructure.config import Settings

from functools import lru_cache
from typing import Iterator

from fastapi import Depends
from sqlalchemy.orm.session import Session

from app.infrastructure.sqlite.database import create_tables, SessionLocal
from app.infrastructure.sqlite.school.school_repository import SchoolRepositoryImpl
from app.infrastructure.sqlite.user.user_repository import UserRepositoryImpl

# create database
create_tables()


def get_session() -> Iterator[Session]:
    session: Session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@lru_cache()
def get_settings() -> Settings:
    return Settings()


def user_repository_dependency(session: Session = Depends(get_session)) -> UserRepository:
    return UserRepositoryImpl(session)


def user_command_usecase(
        user_repository: UserRepository = Depends(user_repository_dependency)
) -> UserCommandUseCase:
    return UserCommandUseCaseImpl(
        user_repository=user_repository
    )


def school_repository_dependency(session: Session = Depends(get_session)) -> SchoolRepository:
    return SchoolRepositoryImpl(session)


def school_command_usecase(
        school_repository: SchoolRepository = Depends(school_repository_dependency)
) -> SchoolCommandUseCase:
    return SchoolCommandUseCaseImpl(
        school_repository=school_repository
    )

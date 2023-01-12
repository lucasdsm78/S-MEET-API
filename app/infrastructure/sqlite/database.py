from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.infrastructure.config import Settings

settings = Settings()

engine = create_engine(
    settings.sqlalchemy_database_url,
    connect_args={
        "check_same_thread": False,
    },
)

SessionLocal = sessionmaker(
    bind=engine,
    autocommit=False,
    autoflush=False,
)

Base = declarative_base()


def create_tables():
    Base.metadata.create_all(bind=engine)
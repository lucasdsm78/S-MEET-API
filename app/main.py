from fastapi import FastAPI

from app.dependency_injections import get_settings
from app.infrastructure.sqlite import database
from app.infrastructure.sqlite.database import engine
from app.presentation.user.user_router import router as user_router
from app.presentation.school.school_router import router as school_router

settings = get_settings()
app = FastAPI()

# Add all routers

app.include_router(user_router)
app.include_router(school_router)

# create the database and import models

database.Base.metadata.create_all(engine)

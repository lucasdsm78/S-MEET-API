from fastapi import FastAPI

from app.dependency_injections import get_settings
from app.infrastructure.sqlite import database
from app.infrastructure.sqlite.database import engine
from app.presentation.user.user_router import router as user_router
from app.presentation.user.bio.user_bio_router import router as user_bio_router
from app.presentation.school.school_router import router as school_router
from app.presentation.activity.activity_router import router as activity_router
from app.presentation.chat.chat_router import router as chat_router
from app.presentation.quiz.quiz_router import router as quiz_router
from app.presentation.smeet.smeet_router import router as smeet_router

settings = get_settings()
app = FastAPI()

# Add all routers

app.include_router(user_router)
app.include_router(user_bio_router)
app.include_router(school_router)
app.include_router(activity_router)
app.include_router(chat_router)
app.include_router(quiz_router)
app.include_router(smeet_router)

# create the database and import models

database.Base.metadata.create_all(engine)

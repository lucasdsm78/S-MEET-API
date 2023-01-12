from fastapi import FastAPI, HTTPException
from fastapi.requests import Request
from fastapi.responses import JSONResponse, PlainTextResponse

from exceptions import StoryException


def add_user_exception_handler(app: FastAPI):
    @app.exception_handler(StoryException)
    async def story_exception_handler(request: Request, exception: StoryException):
        return JSONResponse(
            status_code=418,
            content={'detail': exception.name}
        )

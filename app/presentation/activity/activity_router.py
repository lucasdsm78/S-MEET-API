from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.application.activities.activity_command_model import ActivityCreateResponse, ActivityCreateModel
from app.application.activities.activity_command_usecase import ActivityCommandUseCase
from app.dependency_injections import activity_command_usecase

router = APIRouter(
    tags=['activity']
)


@router.post(
    "/activity/create",
    response_model=ActivityCreateResponse,
    summary="Create an activity",
    status_code=status.HTTP_200_OK,
)
async def create_activity(
        data: ActivityCreateModel,
        activity_command_usecase: ActivityCommandUseCase = Depends(activity_command_usecase),
):
    try:
        activity = activity_command_usecase.create(data)

    except Exception as e:
        raise

    return activity
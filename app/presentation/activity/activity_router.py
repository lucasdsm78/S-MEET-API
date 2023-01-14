from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.params import Path

from app.application.activities.activity_command_model import ActivityCreateResponse, ActivityCreateModel
from app.application.activities.activity_command_usecase import ActivityCommandUseCase
from app.application.activities.activity_query_model import ActivityReadModel
from app.application.activities.activity_query_usecase import ActivityQueryUseCase
from app.dependency_injections import activity_command_usecase, activity_query_usecase, current_user
from app.domain.activity.exception.activity_exception import ActivitiesNotFoundError, ActivityNotFoundError
from app.presentation.activity.activity_error_message import ErrorMessageActivitiesNotFound, \
    ErrorMessageActivityNotFound

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
        current_user: dict = Depends(current_user)
):
    try:
        activity = activity_command_usecase.create(current_user.get('email', ''), data)

    except Exception as e:
        raise

    return activity


@router.get(
    "/activities",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivitiesNotFound,
        }
    }
)
async def get_activities(
        activity_query_usecase: ActivityQueryUseCase = Depends(activity_query_usecase),
):
    try:
        activities = activity_query_usecase.fetch_activities()

    except Exception as e:
        raise

    if not len(activities.get("activities")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=ActivitiesNotFoundError.message,
        )

    return activities


@router.get(
    "/activity/{id}",
    response_model=ActivityReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivityNotFound,
        },
    },
)
async def get_activity(
        activity_id: int,
        activity_query_usecase: ActivityQueryUseCase = Depends(activity_query_usecase),

):
    try:
        activity = activity_query_usecase.get_activity_by_id(activity_id)
    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return activity



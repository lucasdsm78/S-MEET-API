from typing import Union, Annotated

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from fastapi.responses import FileResponse
from fastapi.params import Path

from app.application.activities.activity_command_model import ActivityCreateResponse, ActivityCreateModel, \
    ActivityParticipateResponse, ActivityCancelParticipationResponse
from app.application.activities.activity_command_usecase import ActivityCommandUseCase
from app.application.activities.activity_query_model import ActivityReadModel
from app.application.activities.activity_query_usecase import ActivityQueryUseCase
from app.dependency_injections import activity_command_usecase, activity_query_usecase, current_user, file_uploader_dependency
from app.domain.activity.exception.activity_exception import ActivitiesNotFoundError, ActivityNotFoundError
from app.domain.services.file_uploader.file_uploader import FileUploader
from app.domain.user.exception.user_exception import UserNotFoundError
from app.presentation.activity.activity_error_message import ErrorMessageActivitiesNotFound, \
    ErrorMessageActivityNotFound
from app.presentation.user.user_error_message import ErrorMessageUserNotFound

router = APIRouter(
    tags=['activity']
)


@router.post(
    "/activity/create",
    response_model=str,
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

@router.post(
    "/activity/image/upload",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivityNotFound,
        }
    }
)
async def upload_image_activity(
        activity_uuid: str,
        image: UploadFile = File(...),
        file_uploader: FileUploader = Depends(file_uploader_dependency),
        current_user: dict = Depends(current_user)
):
    try:
        image_filename = file_uploader.save_image_file('activity', image, activity_uuid)

    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return image_filename

@router.get(
    "/activity/image/{activity_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivityNotFound,
        }
    }
)
async def get_image(
        activity_id: int,
        activity_query_usecase: ActivityQueryUseCase = Depends(activity_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        return activity_query_usecase.get_image_activity(activity_id)

    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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
        current_user: dict = Depends(current_user),
):
    try:
        activity = activity_query_usecase.get_activity_by_id(activity_id, current_user.get('email', ''))
    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return activity


@router.post(
    "/activity/{id}/participate",
    response_model=ActivityParticipateResponse,
    summary="Participate to an activity",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": Union[ErrorMessageActivityNotFound, ErrorMessageUserNotFound]
        },
    },
)
async def participate_activity(
        activity_id: int,
        activity_command_usecase: ActivityCommandUseCase = Depends(activity_command_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        activity_participant = activity_command_usecase.add_participant(activity_id, current_user.get('email', ''))

    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return activity_participant


@router.delete(
    "/activity/{id}/participation/cancel",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Cancel a participation to an activity",
    response_model=ActivityCancelParticipationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivityNotFound,
        },
    },
)
async def cancel_participation_activity(
        activity_id: int,
        activity_command_usecase: ActivityCommandUseCase = Depends(activity_command_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        cancel_participation_activity = activity_command_usecase.delete_participant(
            activity_id,
            current_user.get('email', '')
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return cancel_participation_activity


@router.get(
    "/activity/{id}/check_participation",
    status_code=status.HTTP_200_OK,
    summary="Check a participation to an activity",
    response_model=bool,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageActivityNotFound,
        },
    },
)
async def check_participation_activity(
        activity_id: int,
        activity_query_usecase: ActivityQueryUseCase = Depends(activity_query_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        check_participation = activity_query_usecase.check_is_participate(
            activity_id,
            current_user.get('id', '')
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except ActivityNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return check_participation

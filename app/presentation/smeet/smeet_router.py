from fastapi import APIRouter, Depends, HTTPException, status
from app.application.activities.activity_query_usecase import ActivityQueryUseCase
from app.application.smeet.smeet_command_model import SmeetCreateModel, SmeetCreateResponse
from app.application.smeet.smeet_command_usecase import SmeetCommandUseCase
from app.application.smeet.smeet_query_usecase import SmeetQueryUseCase
from app.dependency_injections import smeet_command_usecase, smeet_query_usecase, current_user
from app.domain.smeet.exception.smeet_exception import SmeetsNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError
from app.presentation.smeet.smeet_error_message import ErrorMessageSmeetsNotFound

router = APIRouter(
    tags=['smeet']
)


@router.post(
    "/smeet/send",
    response_model=SmeetCreateResponse,
    summary="Send a smeet",
    status_code=status.HTTP_200_OK,
)
async def send_smeet(
        user_receiver: int,
        data: SmeetCreateModel,
        smeet_command_usecase: SmeetCommandUseCase = Depends(smeet_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        smeet = smeet_command_usecase.create(current_user.get('id', ''), user_receiver, data)

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )

    return smeet


@router.get(
    "/smeets",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageSmeetsNotFound,
        }
    }
)
async def get_smeets(
        smeet_query_usecase: SmeetQueryUseCase = Depends(smeet_query_usecase),
):
    try:
        smeets = smeet_query_usecase.fetch_smeets()

    except Exception as e:
        print(e)
        raise

    if not len(smeets.get("smeets")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SmeetsNotFoundError.message,
        )

    return smeets


@router.get(
    "/smeets/sent",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageSmeetsNotFound,
        }
    }
)
async def get_smeets_sent(
        current_user: dict = Depends(current_user),
        smeet_query_usecase: SmeetQueryUseCase = Depends(smeet_query_usecase),
):
    try:
        smeets = smeet_query_usecase.fetch_smeets_sent(current_user.get('id', ''))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )

    if not len(smeets.get("smeets")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SmeetsNotFoundError.message,
        )

    return smeets

@router.get(
    "/smeets/receive",
    response_model=dict,
    summary="Get smeets for user connected",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageSmeetsNotFound,
        }
    }
)
async def get_smeets_receive(
        current_user: dict = Depends(current_user),
        smeet_query_usecase: SmeetQueryUseCase = Depends(smeet_query_usecase),
):
    try:
        smeets = smeet_query_usecase.fetch_smeets_receive(current_user.get('id', ''))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not len(smeets.get("smeets")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SmeetsNotFoundError.message,
        )

    return smeets

@router.get(
    "/smeets/user/{id}/receive",
    response_model=dict,
    summary="Get smeets for a user by this id",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageSmeetsNotFound,
        }
    }
)
async def get_smeets_receive_by_user_id(
        id: int,
        smeet_query_usecase: SmeetQueryUseCase = Depends(smeet_query_usecase),
):
    try:
        smeets = smeet_query_usecase.fetch_smeets_receive(id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not len(smeets.get("smeets")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=SmeetsNotFoundError.message,
        )

    return smeets
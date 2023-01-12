from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.application.user.user_command_model import UserCreateResponse, UserCreateModel
from app.application.user.user_command_usecase import UserCommandUseCase
from app.dependency_injections import user_command_usecase
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError
from app.presentation.user.user_error_message import ErrorMessageUserEmailAlreadyExists

router = APIRouter(
    tags=['user']
)


@router.post(
    "/user/create",
    response_model=UserCreateResponse,
    summary="Create a user",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageUserEmailAlreadyExists,
        },
    },
)
async def create_user(
        data: UserCreateModel,
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    try:
        user = user_command_usecase.create(data)

    except UserEmailAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    except Exception as e:
        print(e)
        raise

    return user

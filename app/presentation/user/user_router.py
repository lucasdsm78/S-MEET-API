from fastapi import APIRouter, Depends, HTTPException, status, Query

from app.application.user.user_command_model import UserCreateResponse, UserCreateModel, UserLoginResponse, \
    UserLoginModel
from app.application.user.user_command_usecase import UserCommandUseCase
from app.application.user.user_query_model import UserReadModel
from app.application.user.user_query_usecase import UserQueryUseCase
from app.dependency_injections import user_command_usecase, user_query_usecase
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UsersNotFoundError, UserNotFoundError
from app.presentation.user.user_error_message import ErrorMessageUserEmailAlreadyExists, ErrorMessageUsersNotFound, \
    ErrorMessageUserNotFound

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


@router.get(
    "/users",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUsersNotFound,
        }
    }
)
async def get_users(
        user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        users = user_query_usecase.fetch_users()

    except Exception as e:
        print(e)
        raise

    if not len(users.get("users")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UsersNotFoundError.message,
        )

    return users


@router.post(
    "/user/login",
    response_model=UserLoginResponse
)
async def login(
        user_login_model: UserLoginModel,
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
):
    return user_command_usecase.login(user_login_model).for_login()


@router.get(
    "/user/profile/{id}",
    response_model=UserReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def get_profile(
        user_id: int,
        user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        user = user_query_usecase.fetch_user_by_id(user_id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user

from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File

from app.application.user.user_command_model import UserCreateResponse, UserCreateModel, UserLoginResponse, \
    UserLoginModel, UserDeleteResponse, UserUpdateModel
from app.application.user.user_command_usecase import UserCommandUseCase
from app.application.user.user_query_model import UserReadModel
from fastapi.responses import FileResponse
from app.application.user.user_query_usecase import UserQueryUseCase
from app.dependency_injections import user_command_usecase, user_query_usecase, file_uploader_dependency, current_user
from app.domain.services.file_uploader.file_uploader import FileUploader
from app.domain.user.exception.user_exception import UserEmailAlreadyExistsError, UsersNotFoundError, UserNotFoundError
from app.presentation.user.user_error_message import ErrorMessageUserEmailAlreadyExists, ErrorMessageUsersNotFound, \
    ErrorMessageUserNotFound

router = APIRouter(
    tags=['user']
)


@router.post(
    "/user/create",
    response_model=UserLoginResponse,
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


@router.post(
    "/user/image/upload",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        }
    }
)
async def upload_image_profil(
        user_uuid: str,
        image: UploadFile = File(...),
        file_uploader: FileUploader = Depends(file_uploader_dependency),
):
    try:
        image_filename = file_uploader.save_image_file('user', image, user_uuid)

    except UserNotFoundError as e:
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
    "/user/image/{user_id}",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        }
    }
)
async def get_image_profil(
        user_id: int,
        user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        return user_query_usecase.get_image_user(user_id)

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )


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


@router.get(
    "/users/activity/{id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUsersNotFound,
        }
    }
)
async def get_users_by_activity(
        activity_id: int,
        user_query_usecase: UserQueryUseCase = Depends(user_query_usecase),
):
    try:
        users = user_query_usecase.fetch_users_by_activity(activity_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

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


@router.delete(
    "/user/{id}/delete",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Delete a user",
    response_model=UserDeleteResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def delete_user(
        id: int,
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        delete_user = user_command_usecase.delete_user(id)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return delete_user


@router.patch(
    "/user/{user_id}/update",
    response_model=UserReadModel,
    summary="Update a user with new pseudo or new image profile",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserNotFound,
        },
    },
)
async def update_user(
        user_id: int,
        pseudo: Optional[str] = None,
        image: UploadFile = None,
        user_command_usecase: UserCommandUseCase = Depends(user_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        updated_user = user_command_usecase.update_user(user_id, pseudo, image)
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return updated_user
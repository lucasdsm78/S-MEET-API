from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File

from app.application.friend.friend_command_model import FriendAddModel, FriendRemoveResponse, FriendRemoveModel, \
    FriendAddResponse, FriendUpdateResponse
from app.application.friend.friend_command_usecase import FriendCommandUseCase
from app.application.friend.friend_query_model import FriendReadModel
from app.application.friend.friend_query_usecase import FriendQueryUseCase
from app.dependency_injections import friend_command_usecase, friend_query_usecase, current_user
from app.domain.friend.exception.friend_exception import FriendAlreadyExistsError, FriendsNotFoundError, \
    FriendNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError
from app.presentation.friend.friend_error_message import ErrorMessageFriendsNotFound, \
    ErrorMessageFriendNotFound, ErrorMessageFriendAlreadyExists

router = APIRouter(
    tags=['friend']
)


@router.post(
    "/friend/add",
    response_model=FriendAddResponse,
    summary="Add a friend",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageFriendAlreadyExists,
        },
    },
)
async def add_friend(
        user_id: int,
        friend_command_usecase: FriendCommandUseCase = Depends(friend_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        friend = friend_command_usecase.add(current_user.get('id', ''), user_id)

    except FriendAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise

    return friend


@router.delete(
    "/friend/{id}/remove",
    response_model=FriendRemoveResponse,
    summary="Remove a friend",
    status_code=status.HTTP_202_ACCEPTED,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageFriendNotFound,
        },
    },
)
async def remove_friend(
        user_id: int,
        friend_command_usecase: FriendCommandUseCase = Depends(friend_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        delete_friend = friend_command_usecase.remove(current_user.get('id', ''), user_id)

    except FriendNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )

    return delete_friend


@router.get(
    "/friends",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageFriendsNotFound,
        }
    }
)
async def get_friends(
        friend_query_usecase: FriendQueryUseCase = Depends(friend_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        friends = friend_query_usecase.get_friends(current_user.get('id', ''))

    except Exception as e:
        raise

    if not len(friends.get("friends")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FriendsNotFoundError.message,
        )

    return friends


@router.get(
    "/friend/status/{user_id}",
    response_model=bool,
    status_code=status.HTTP_200_OK
)
async def get_status(
        user_id: int,
        friend_query_usecase: FriendQueryUseCase = Depends(friend_query_usecase),
        current_user: dict = Depends(current_user),
):
    return friend_query_usecase.get_status(current_user.get('id', ''), user_id)
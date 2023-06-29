from fastapi import APIRouter, Depends, HTTPException, status, Query, UploadFile, File

from app.application.friend.friend_command_model import FriendCreateResponse, FriendCreateModel, FriendAddResponse, \
    FriendAddModel, FriendRemoveResponse, FriendRemoveModel
from app.application.friend.friend_command_usecase import FriendCommandUseCase
from app.application.friend.friend_query_model import FriendReadModel
from app.application.friend.friend_query_usecase import FriendQueryUseCase
from app.dependency_injections import friend_command_usecase, friend_query_usecase, current_friend
from app.domain.friend.exception.friend_exception import FriendAlreadyExistsError, FriendsNotFoundError, \
    FriendNotFoundError
from app.presentation.friend.friend_error_message import ErrorMessageFriendAlreadyExists, ErrorMessageFriendsNotFound, \
    ErrorMessageFriendNotFound

router = APIRouter(
    tags=['friend']
)


@router.post(
    "/friend/add/{id}",
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
        data: FriendAddModel,
        friend_command_usecase: FriendCommandUseCase = Depends(friend_command_usecase),
):
    try:
        friend = friend_command_usecase.add(data)

    except FriendAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    except Exception as e:
        print(e)
        raise

    return friend


@router.delete(
    "/friend/remove/{id}",
    response_model=FriendRemoveResponse,
    summary="Remove a friend",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageFriendNotFound,
        },
    },
)
async def remove_friend(
        data: FriendRemoveModel,
        friend_command_usecase: FriendCommandUseCase = Depends(friend_command_usecase),
):
    try:
        friend = friend_command_usecase.remove(data.id)

    except ErrorMessageFriendNotFound as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        print(e)
        raise

    return friend


@router.get(
    "/friend/friends",
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
):
    try:
        friends = friend_query_usecase.get_friends()

    except Exception as e:
        print(e)
        raise

    if not len(friends.get("friend")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=FriendsNotFoundError.message,
        )

    return friends

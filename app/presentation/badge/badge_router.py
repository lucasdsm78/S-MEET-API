from fastapi import APIRouter, Depends, HTTPException, status
from app.application.badge.badge_command_model import BadgeCreateModel, BadgeCreateResponse, BadgeUpdateResponse, \
    BadgeUpdateModel
from app.application.badge.badge_command_usecase import BadgeCommandUseCase
from app.application.badge.badge_query_usecase import BadgeQueryUseCase
from app.dependency_injections import current_user, badge_command_usecase, badge_query_usecase
from app.domain.badge.exception.badge_exception import BadgesNotFoundError, BadgeNotFoundError
from app.presentation.badge.badge_error_message import ErrorMessageBadgesNotFound

router = APIRouter(
    tags=['badge']
)


@router.post(
    "/badge/create",
    response_model=BadgeCreateResponse,
    summary="Create a badge",
    status_code=status.HTTP_200_OK,
)
async def create_badge(
        data: BadgeCreateModel,
        badge_command_usecase: BadgeCommandUseCase = Depends(badge_command_usecase),
):
    try:
        badge = badge_command_usecase.create(data)

    except Exception as e:
        print(e)
        raise

    return badge


@router.patch(
    "/badge/{id}/update",
    response_model=BadgeUpdateResponse,
    summary="Update badge with a new name",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_badge(
        badge_id: int,
        data: BadgeUpdateModel,
        badge_command_usecase: BadgeCommandUseCase = Depends(badge_command_usecase),
):
    try:
        update_badge = badge_command_usecase.update_badge(badge_id, data)
    except BadgeNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    return update_badge


@router.get(
    "/badges",
    response_model=dict,
    summary="Get all badges available in the app",
    description="API call to get all badges available in the app",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBadgesNotFound,
        }
    }
)
async def get_badges(
        badge_query_usecase: BadgeQueryUseCase = Depends(badge_query_usecase),
):
    try:
        badges = badge_query_usecase.fetch_badges()

    except Exception as e:
        raise

    if not len(badges.get("badges")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BadgesNotFoundError.message,
        )

    return badges



@router.get(
    "/badges/users",
    response_model=dict,
    summary="Get all badges for all users",
    description="API call to get all badges for all users in the app",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBadgesNotFound,
        }
    }
)
async def get_user_badges(
        badge_query_usecase: BadgeQueryUseCase = Depends(badge_query_usecase),
):
    try:
        user_badges = badge_query_usecase.fetch_user_badges()

    except Exception as e:
        raise

    if not len(user_badges.get("user_badges")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BadgesNotFoundError.message,
        )

    return user_badges

@router.get(
    "/badges/user",
    response_model=dict,
    summary="Get badges user connected",
    description="API call to get all badges for user connected",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBadgesNotFound,
        }
    }
)
async def get_badges_user_connected(
        badge_query_usecase: BadgeQueryUseCase = Depends(badge_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        badges = badge_query_usecase.fetch_badges_by_user_id(current_user.get('id', ''))

    except Exception as e:
        raise

    if not len(badges.get("badges")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BadgesNotFoundError.message,
        )

    return badges


@router.get(
    "/badges/user/{id}",
    response_model=dict,
    summary="Get all badges for a user",
    description="Get all badges for a user by this id",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBadgesNotFound,
        }
    }
)
async def get_badges_by_user_id(
        id: int,
        badge_query_usecase: BadgeQueryUseCase = Depends(badge_query_usecase),
):
    try:
        badges = badge_query_usecase.fetch_badges_by_user_id(id)

    except Exception as e:
        raise

    if not len(badges.get("badges")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=BadgesNotFoundError.message,
        )

    return badges
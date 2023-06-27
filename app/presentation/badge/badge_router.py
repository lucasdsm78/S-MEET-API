from fastapi import APIRouter, Depends, HTTPException, status
from app.application.badge.badge_command_model import BadgeCreateModel, BadgeCreateResponse
from app.application.badge.badge_command_usecase import BadgeCommandUseCase
from app.application.badge.badge_query_usecase import BadgeQueryUseCase
from app.dependency_injections import current_user, badge_command_usecase, badge_query_usecase
from app.domain.badge.exception.badge_exception import BadgesNotFoundError
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


@router.get(
    "/badges",
    response_model=dict,
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
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageBadgesNotFound,
        }
    }
)
async def get_badges_by_user_id(
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
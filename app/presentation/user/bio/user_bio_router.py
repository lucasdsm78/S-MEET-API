from fastapi import APIRouter, Depends, HTTPException, status

from app.application.user.bio.user_bio_command_model import UserBioUpdateResponse, UserBioCreateModel
from app.application.user.bio.user_bio_command_usecase import UserBioCommandUseCase
from app.application.user.bio.user_bio_query_model import UserBioReadModel
from app.application.user.bio.user_bio_query_usecase import UserBioQueryUseCase
from app.dependency_injections import user_bio_command_usecase, user_bio_query_usecase, current_user
from app.domain.user.exception.user_exception import UserBioNotFoundError
from app.presentation.user.user_error_message import ErrorMessageUserBioNotFound

router = APIRouter(
    tags=['user_bio']
)


@router.post(
    "/user/bio/update",
    response_model=UserBioUpdateResponse,
    summary="Update a user bio",
    status_code=status.HTTP_200_OK,
)
async def update_user_bio(
        data: UserBioCreateModel,
        user_bio_command_usecase: UserBioCommandUseCase = Depends(user_bio_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        user_bio = user_bio_command_usecase.update(current_user.get('id', ''), data)

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )

    return user_bio


@router.get(
    "/user/bio/{id}",
    response_model=UserBioReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUserBioNotFound,
        },
    },
)
async def get_user_bio_by_user_id(
        user_id: int,
        user_bio_query_usecase: UserBioQueryUseCase = Depends(user_bio_query_usecase),
):
    try:
        user_bio = user_bio_query_usecase.fetch_user_bio_by_user_id(user_id)
    except UserBioNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return user_bio

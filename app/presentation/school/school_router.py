from fastapi import APIRouter, Depends, HTTPException, status

from app.application.school.school_command_model import SchoolCreateModel, SchoolCreateResponse
from app.application.school.school_command_usecase import SchoolCommandUseCase
from app.dependency_injections import school_command_usecase
from app.domain.school.exception.school_exception import SchoolNamelAlreadyExistsError
from app.presentation.school.school_error_message import ErrorMessageSchoolNameAlreadyExists

router = APIRouter(
    tags=['school']
)


@router.post(
    "/school/create",
    response_model=SchoolCreateResponse,
    summary="Create a school",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_409_CONFLICT: {
            "model": ErrorMessageSchoolNameAlreadyExists,
        },
    },
)
async def create_school(
        data: SchoolCreateModel,
        school_command_usecase: SchoolCommandUseCase = Depends(school_command_usecase),
):
    try:
        school = school_command_usecase.create(data)

    except SchoolNamelAlreadyExistsError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=e.message,
        )

    except Exception as e:
        print(e)
        raise

    return school

from typing import Union

from fastapi import APIRouter, Depends, HTTPException, status, Query, Body
from app.application.quiz.quiz_command_model import QuizCreateResponse, QuizCreateModel, ScoreAddedResponse, \
    ScoreCreateModel
from app.application.quiz.quiz_command_usecase import QuizCommandUseCase
from app.application.quiz.quiz_query_model import QuizReadModel
from app.application.quiz.quiz_query_usecase import QuizQueryUseCase
from app.dependency_injections import current_user, quiz_command_usecase, quiz_query_usecase
from app.domain.quiz.exception.quiz_exception import QuizsNotFoundError, ScoreNotFoundError, QuizNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError
from app.presentation.quiz.quiz_error_message import ErrorMessageQuizsNotFound, ErrorMessageQuestionsNotFound, \
    ErrorMessageScoreNotFound, ErrorMessageQuizNotFound

router = APIRouter(
    tags=['quiz']
)


@router.post(
    "/quiz/create",
    response_model=QuizCreateResponse,
    summary="Create a quiz",
    status_code=status.HTTP_200_OK,
)
async def create_quiz(
        data: QuizCreateModel,
        quiz_command_usecase: QuizCommandUseCase = Depends(quiz_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        quiz = quiz_command_usecase.create(current_user.get('email', ''), data)

    except Exception as e:
        raise

    return quiz


@router.get(
    "/questions/{quiz_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageQuestionsNotFound,
        }
    }
)
async def get_questions_by_quiz_id(
        quiz_id: int,
        quiz_query_usecase: QuizQueryUseCase = Depends(quiz_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        questions = quiz_query_usecase.fetch_questions_by_quiz_id(quiz_id)

    except Exception as e:
        raise

    if not len(questions.get("questions")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=QuizsNotFoundError.message,
        )

    return questions


@router.get(
    "/quizs",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageQuizsNotFound,
        }
    }
)
async def get_quizs(
        quiz_query_usecase: QuizQueryUseCase = Depends(quiz_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        quizs = quiz_query_usecase.fetch_quizs_by_user_id(current_user.get('id', ''))

    except Exception as e:
        raise

    if not len(quizs.get("quizs")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=QuizsNotFoundError.message,
        )

    return quizs


@router.post(
    "/quiz/{quiz_id}/score/add",
    response_model=ScoreAddedResponse,
    summary="Add a score to a quiz",
    status_code=status.HTTP_200_OK,
)
async def add_score(
        quiz_id: int,
        data: ScoreCreateModel,
        quiz_command_usecase: QuizCommandUseCase = Depends(quiz_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        score = quiz_command_usecase.add_score(current_user.get('id', ''), quiz_id, data)

    except Exception as e:
        raise

    return score


@router.get(
    "/quiz/{quiz_id}/score",
    response_model=int,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageScoreNotFound,
        },
    },
)
async def get_score(
        quiz_id: int,
        quiz_query_usecase: QuizQueryUseCase = Depends(quiz_query_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        score = quiz_query_usecase.fetch_score(quiz_id, current_user.get('id', ''))
    except ScoreNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except QuizNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    return score


@router.get(
    "/quiz/{quiz_id}",
    response_model=QuizReadModel,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageQuizNotFound,
        },
    },
)
async def get_quiz_by_id(
        quiz_id: int,
        quiz_query_usecase: QuizQueryUseCase = Depends(quiz_query_usecase),
):
    try:
        quiz = quiz_query_usecase.fetch_quiz_by_id(quiz_id)
    except QuizNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return quiz

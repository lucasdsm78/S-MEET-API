from fastapi import APIRouter, Depends, HTTPException, status
from app.application.notification.notification_command_model import NotificationCreateResponse, NotificationCreateModel, \
    NotificationUpdateResponse
from app.application.notification.notification_command_usecase import NotificationCommandUseCase
from app.application.notification.notification_query_usecase import NotificationQueryUseCase
from app.dependency_injections import notification_command_usecase, notification_query_usecase, current_user
from app.domain.notification.exception.notification_exception import NotificationsNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError
from app.presentation.notification.notification_error_message import ErrorMessageNotificationsNotFound

router = APIRouter(
    tags=['notification']
)


@router.post(
    "/notification/create",
    response_model=NotificationCreateResponse,
    summary="Create a notification",
    status_code=status.HTTP_200_OK,
)
async def create_notification(
        data: NotificationCreateModel,
        notification_command_usecase: NotificationCommandUseCase = Depends(notification_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        notification = notification_command_usecase.create(data, current_user.get('email', ''))

    except Exception as e:
        raise

    return notification

@router.patch(
    "/notifications/update",
    response_model=NotificationUpdateResponse,
    summary="Update notifications not read at true",
    status_code=status.HTTP_202_ACCEPTED,
)
async def update_notifications(
        notification_command_usecase: NotificationCommandUseCase = Depends(notification_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        update_notifications = notification_command_usecase.update_notif(current_user.get('id', ''))
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=e
        )
    return update_notifications


@router.get(
    "/notifications",
    response_model=dict,
    summary="Get all notifications for all users in the app",
    description="API call to get all notifications for all users in the app",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageNotificationsNotFound,
        }
    }
)
async def get_notifications(
        notification_query_usecase: NotificationQueryUseCase = Depends(notification_query_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        notifications = notification_query_usecase.fetch_notifications()

    except Exception as e:
        raise

    if not len(notifications.get("notifications")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotificationsNotFoundError.message,
        )

    return notifications

@router.get(
    "/notifications/user",
    response_model=dict,
    summary="Get notifications user connected",
    description="API call to get all notifications for user connected",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageNotificationsNotFound,
        }
    }
)
async def get_notifications_user_connected(
        notification_query_usecase: NotificationQueryUseCase = Depends(notification_query_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        notifications = notification_query_usecase.fetch_notifications_by_user_id(current_user.get('id', ''))

    except Exception as e:
        raise

    if not len(notifications.get("notifications")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=NotificationsNotFoundError.message,
        )

    return notifications
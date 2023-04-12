from typing import Dict, Union, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.application.chat.message.message_command_model import MessageCreateResponse, MessageCreateModel
from app.application.chat.message.message_command_usecase import MessageCommandUseCase
from app.application.chat.message.message_query_usecase import MessageQueryUseCase
from app.application.chat.room.room_command_model import RoomCreateResponse, RoomCreateModel, RoomParticipateResponse, \
    RoomCancelParticipationResponse
from app.application.chat.room.room_command_usecase import RoomCommandUseCase
from app.application.chat.room.room_query_usecase import RoomQueryUseCase
from app.dependency_injections import current_user, room_repository_dependency, room_command_usecase, \
    room_query_usecase, message_repository_dependency, message_command_usecase, message_query_usecase
from app.domain.chat.message.exception.message_exception import MessagesNotFoundError
from app.domain.chat.message.model.message import Message
from app.domain.chat.room.exception.room_exception import RoomNotFoundError, RoomsNotFoundError
from app.domain.user.exception.user_exception import UserNotFoundError, UsersNotFoundError
from app.infrastructure.services.socket_manager.socket_manager import SocketManagerImpl
from app.presentation.chat.chat_error_message import ErrorMessageRoomNotFound, ErrorMessageRoomsNotFound
from app.presentation.user.user_error_message import ErrorMessageUserNotFound, ErrorMessageUsersNotFound, \
    ErrorMessagesRoomNotFound

router = APIRouter(
    tags=['chat']
)

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <h2>Your ID: <span id="ws-id"></span></h2>
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var client_id = 1
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/room/${client_id}`);
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
    </body>
</html>
"""

manager = SocketManagerImpl()

connections: Dict[str, WebSocket] = {}


@router.get("/chat")
async def get():
    return HTMLResponse(html)


@router.websocket("/room/{room_id}")
async def room_endpoint(
        websocket: WebSocket,
        room_id: int,
        room_query_usecase: RoomQueryUseCase = Depends(room_repository_dependency),
        # message_command_usecase: MessageCommandUseCase = Depends(message_repository_dependency),
        current_user: dict = Depends(current_user)
):
    room = room_query_usecase.find_room_by_id(room_id)
    if not room:
        await websocket.close()
        return

    for user in room.users:
        connections[user.username] = websocket

    await websocket.accept()

    for message in room.messages:
        await websocket.send_json(message.__dict__)

    try:
        while True:
            data = await websocket.receive_text()

            message = Message(
                content=data,
                room_id=room_id,
                user_id=current_user.get('id', '')
            )

            # message_command_usecase.create(message)
            room.messages.append(message)

            for user in room.users:
                await connections[user.username].send_text(f"{user.username}: {data}")

            # for conn, id in connections.items():
            #  if uid != user_id:
            # await manager.send_personal_message(f"You wrote: {data}", websocket)
            # await manager.broadcast(f"Client #{current_user.get('email', '')} says: {data}")

    except WebSocketDisconnect:
        manager.disconnect(websocket)
        room.remove_user(websocket)
        await manager.broadcast(f"Client #{current_user.get('email', '')} left the chat")


@router.websocket("/ws/{user_id}")
async def websocket_endpoint(websocket: WebSocket, user_id: str):
    await manager.connect(websocket)
    print("Connection added")

    try:
        while True:
            data = await websocket.receive_text()
            # for conn, id in connections.items():
            #  if uid != user_id:
            await manager.send_personal_message(f"You wrote: {data}", websocket)
            await manager.broadcast(f"Client #{user_id} says: {data}")
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        await manager.broadcast(f"Client #{user_id} left the chat")


@router.post(
    "/room/create",
    response_model=RoomCreateResponse,
    summary="Create a room",
    status_code=status.HTTP_200_OK
)
async def create_room(
        data: RoomCreateModel,
        room_command_usecase: RoomCommandUseCase = Depends(room_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        room = room_command_usecase.create(data, current_user.get('school_id', ''), current_user.get('id', ''))

    except Exception as e:
        raise

    return room


@router.post(
    "/room/{room_id}/participate",
    response_model=RoomParticipateResponse,
    summary="Participate to a room",
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": Union[ErrorMessageRoomNotFound, ErrorMessageUserNotFound]
        },
    },
)
async def participate_room(
        room_id: int,
        room_command_usecase: RoomCommandUseCase = Depends(room_command_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        room_participant = room_command_usecase.add_participant_room(room_id, current_user.get('id', ''))

    except RoomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return room_participant


@router.delete(
    "/room/{room_id}/participation/cancel",
    status_code=status.HTTP_202_ACCEPTED,
    summary="Cancel a participation to a room",
    response_model=RoomCancelParticipationResponse,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageRoomNotFound,
        },
    },
)
async def cancel_participation_room(
        room_id: int,
        user_id: Optional[int] = None,
        room_command_usecase: RoomCommandUseCase = Depends(room_command_usecase),
        current_user: dict = Depends(current_user),
):
    try:
        id_user = current_user.get('id', '')
        if user_id is not None:
            id_user = user_id

        participation_cancel_room = room_command_usecase.delete_participant_room(
            room_id=room_id,
            user_id=id_user
        )
    except UserNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except RoomNotFoundError as e:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=e.message,
        )

    except Exception as e:
        print(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    return participation_cancel_room


@router.get(
    "/conversations",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageRoomsNotFound,
        }
    }
)
async def get_conversations(
        current_user: dict = Depends(current_user),
        room_query_usecase: RoomQueryUseCase = Depends(room_query_usecase),
):
    try:
        conversations = room_query_usecase.fetch_conversations_by_user(user_id=current_user.get('id', ''))

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not len(conversations.get("conversations")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=RoomsNotFoundError.message,
        )

    return conversations


@router.get(
    "/users/room/{room_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessageUsersNotFound,
        }
    }
)
async def get_participations_by_room(
        room_id: int,
        room_query_usecase: RoomQueryUseCase = Depends(room_query_usecase),
):
    try:
        participations = room_query_usecase.fetch_participations_by_room(room_id=room_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not len(participations.get("participations")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=UsersNotFoundError.message,
        )

    return participations


@router.post(
    "/message/create",
    response_model=MessageCreateResponse,
    summary="Create a message",
    status_code=status.HTTP_200_OK
)
async def create_message(
        data: MessageCreateModel,
        message_command_usecase: MessageCommandUseCase = Depends(message_command_usecase),
        current_user: dict = Depends(current_user)
):
    try:
        message = message_command_usecase.create(data, current_user.get('id', ''))

    except Exception as e:
        raise

    return message


@router.get(
    "/messages/{room_id}",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ErrorMessagesRoomNotFound,
        }
    }
)
async def get_messages_by_room(
        room_id: int,
        message_query_usecase: MessageQueryUseCase = Depends(message_query_usecase),
):
    try:
        messages = message_query_usecase.find_messages_by_room(room_id=room_id)

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        )

    if not len(messages.get("messages")):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=MessagesNotFoundError.message,
        )

    return messages

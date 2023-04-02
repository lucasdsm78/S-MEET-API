from fastapi import APIRouter, Depends, HTTPException, status
from fastapi import WebSocket, WebSocketDisconnect
from fastapi.responses import HTMLResponse

from app.dependency_injections import socket_manager_dependency
from app.domain.services.socket_manager.socket_manager import SocketManager
from app.infrastructure.services.socket_manager.socket_manager import SocketManagerImpl

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
            var client_id = Date.now()
            document.querySelector("#ws-id").textContent = client_id;
            var ws = new WebSocket(`ws://localhost:8000/ws/${client_id}`);
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


@router.get("/chat")
async def get():
    return HTMLResponse(html)


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

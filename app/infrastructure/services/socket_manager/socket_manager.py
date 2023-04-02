from typing import List
from pydantic import BaseModel

from app.domain.services.socket_manager.socket_manager import SocketManager
from fastapi import WebSocket


class SocketManagerImpl(SocketManager, BaseModel):
    active_connections: list[WebSocket] = []

    class Config:
        arbitrary_types_allowed = True

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
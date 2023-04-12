from abc import ABC, abstractmethod
from fastapi import WebSocket


class SocketManager(ABC):

    @abstractmethod
    def connect(self, websocket: WebSocket):
        raise NotImplementedError

    @abstractmethod
    def disconnect(self, websocket: WebSocket):
        raise NotImplementedError

    @abstractmethod
    def broadcast(self, data):
        raise NotImplementedError

    @abstractmethod
    async def send_personal_message(self, message: str, websocket: WebSocket):
        raise NotImplementedError
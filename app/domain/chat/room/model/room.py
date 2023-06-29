from typing import Optional, List

from fastapi import WebSocket

from app.domain.chat.message.model.message import Message


class Room:
    """Room represents your collection of rooms as an entity."""

    def __init__(
            self,
            name: str,
            uuid: str,
            description: str,
            school_id: int,
            image_room: str,
            id: Optional[int] = None,
            created_at: Optional[int] = None,
            updated_at: Optional[int] = None,
    ):
        self.id: Optional[int] = id
        self.name: str = name
        self.description: str = description
        self.uuid: str = uuid
        self.school_id: int = school_id
        self.image_room: str = image_room
        self.messages = []
        self.users = []
        self.created_at: Optional[int] = created_at
        self.updated_at: Optional[int] = updated_at

    def add_user(self, email: str):
        self.users.append(email)

    def remove_user(self, user: WebSocket):
        self.users.remove(user)

    async def broadcast(self, message: Message):
        for user in self.users:
            await user.send_json(message.__dict__)
from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.smeet.model.smeet import Smeet


class SmeetRepository(ABC):
    """SmeetRepository defines a repository interface for Smeet entity."""

    @abstractmethod
    def create(self, smeet: Smeet) -> Optional[Smeet]:
        raise NotImplementedError

    @abstractmethod
    def find_smeets(self) -> List[Smeet]:
        raise NotImplementedError

    @abstractmethod
    def find_smeets_by_user_receiver_id(self, user_receiver_id: int) -> List[Smeet]:
        raise NotImplementedError

    @abstractmethod
    def find_smeets_by_user_sender_id(self, user_sender_id: int) -> List[Smeet]:
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
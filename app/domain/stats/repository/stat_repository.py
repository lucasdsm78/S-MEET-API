from abc import ABC, abstractmethod
from typing import Optional, List

from app.domain.stats.model.stats import Stat


class StatRepository(ABC):
    """StatRepository defines a repository interface for Stats entity."""

    @abstractmethod
    def create(self, stat: Stat) -> Optional[Stat]:
        raise NotImplementedError

    @abstractmethod
    def find_by_id(self, stat_id: int) -> Optional[Stat]:
        raise NotImplementedError

    @abstractmethod
    def find_by_user_id(self, user_id: int) -> Optional[Stat]:
        raise NotImplementedError

    @abstractmethod
    def update_stat(self, stat: Stat) -> Optional[Stat]:
        raise NotImplementedError

    @abstractmethod
    def delete_stat(self, stat_id: int):
        raise NotImplementedError

    @abstractmethod
    def commit(self):
        raise NotImplementedError

    @abstractmethod
    def rollback(self):
        raise NotImplementedError
from abc import ABC, abstractmethod
from typing import Optional

from pymongo.collection import Collection


class Service(ABC):
    def __init__(self, collection: Collection):
        self.collection = collection

    @abstractmethod
    async def get_all(self) -> list:
        pass

    @abstractmethod
    async def create(self, data: dict) -> dict:
        pass

    @abstractmethod
    async def get_by_id(self, item_id: str) -> Optional[dict]:
        pass

    @abstractmethod
    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        pass
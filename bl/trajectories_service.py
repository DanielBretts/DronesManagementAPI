import asyncio
from typing import Optional
from pymongo.collection import Collection
from bson import ObjectId

from bl.service import Service
from schema.schemas import trajectory_serial, trajectory_list_serial


class TrajectoriesService(Service):


    async def get_all(self) -> list:
        return trajectory_list_serial(self.collection.find())

    async def create(self, trajectory: dict) -> dict:
        if await self.is_valid_trajectory(trajectory):
            result = self.collection.insert_one(trajectory)
            inserted_id = result.inserted_id
            inserted_mission = self.collection.find_one({'_id': ObjectId(inserted_id)})
            return trajectory_serial(inserted_mission)
        return dict()

    async def is_valid_trajectory(self, trajectory_data) -> bool:
        results = await asyncio.gather(
            self.is_trajectory_exist(trajectory_data),
            self.is_duration_valid(trajectory_data['distance']),
            self.is_number_of_products_valid(trajectory_data['number_of_products'])
        )
        # Negate the first result to check if the trajectory exist
        results = [not results[0]] + list(results[1:])
        print(results)
        return all(results)

    async def get_by_id(self, mission_id: str) -> dict:
        return self.collection.find_one({"id": mission_id}, {'_id': 0})

    async def is_trajectory_exist(self, trajectory: dict):
        trajectory_entity = await self.get_by_id(trajectory['id'])
        if trajectory_entity is None:
            return False
        return True

    async def is_duration_valid(self, duration: int) -> bool:
        return duration > 0

    async def is_number_of_products_valid(self, num: int):
        return num >= 0

    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        pass

import asyncio
from typing import Optional
from pymongo.collection import Collection
from bson import ObjectId

from bl.service import Service
from schema.schemas import mission_list_serial
from bl.trajectories_service import TrajectoriesService
from config.database import collection_trajectories


class MissionsService(Service):


    async def get_all(self) -> list:
        return mission_list_serial(self.collection.find())

    async def create(self, mission: dict) -> dict:
        if await self.is_valid_mission(mission) is False:
            return dict()
        result = self.collection.insert_one(mission)
        inserted_id = result.inserted_id
        inserted_mission = self.collection.find_one({'_id': ObjectId(inserted_id)}, {'_id': 0})
        return inserted_mission

    async def get_by_id(self, mission_id: str):
        return self.collection.find_one({"id": mission_id}, {'_id': 0})

    async def is_valid_mission(self, mission: dict) -> bool:
        results = await asyncio.gather(
            self.is_mission_id_valid(mission['id']),
            self.is_trajectory_exist(mission['trajectory_id']),
            self.is_valid_duration(mission['duration']),
            self.is_valid_priority(mission['priority'])
        )
        print(results)
        return all(results)

    async def is_mission_id_valid(self, mission_id) -> bool:
        mission_entity = await self.get_by_id(mission_id)
        if mission_entity is None:
            return True
        return False

    async def is_trajectory_exist(self, traj_id: str) -> bool:
        traj_service = TrajectoriesService(collection_trajectories)
        traj = await traj_service.get_by_id(traj_id)
        print(traj)
        return True if traj is not None else False

    async def is_valid_duration(self, num):
        return True if num > 0 else False

    async def is_valid_priority(self, num):
        return True if 0 <= num <= 10 else False

    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        pass

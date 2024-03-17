import asyncio
from typing import Optional
from bson import ObjectId
from bl.service import Service
from bl.service import Service
from schema.schemas import drone_serial, drone_list_serial
from utils.Constants import DroneStatus
from bl.missions_service import MissionsService
from config.database import collection_missions
from utils.logger_config import log


class DronesService(Service):

    async def get_all(self):
        return drone_list_serial(self.collection.find())

    async def get_drones_by_status(self, status: str) -> Optional[list]:
        return list(self.collection.find({"status": status}, {'_id': 0}))

    async def get_by_id(self, drone_id: str) -> Optional[dict]:
        try:
            return self.collection.find_one({"id": drone_id}, {'_id': 0})
        except Exception as e:
            log.error(f"Failed to retrieve drone with ID {drone_id}: {e}")
            return None

    async def update_drone_status(self, drone_id: str, status: str) -> Optional[dict]:
        if await self.is_status_valid(status):
            self.collection.update_one({"id": drone_id}, {"$set": {"status": status}})
            return await self.get_by_id(drone_id)
        else:
            log.error("Invalid status")
            return None

    async def is_status_valid(self, status: str) -> bool:
        return status in DroneStatus.__dict__.values()

    async def create(self, drone_data: dict) -> dict:
        # drone_data['status'] = DroneStatus.AVAILABLE
        # drone_data['current_mission_id'] = None
        if await self.is_valid_drone_data(drone_data) is False:
            return dict()
        # Convert the set to a list before inserting to db
        drone_data['possible_missions_ids'] = list(drone_data["possible_missions_ids"])
        result = self.collection.insert_one(drone_data)
        inserted_id = result.inserted_id
        inserted_drone = self.collection.find_one({"_id": ObjectId(inserted_id)}, {'_id': 0})
        return inserted_drone

    async def modify_possible_missions(self, drone_id: str, possible_missions_ids: list) -> bool:
        missions_service = MissionsService(collection_missions)
        for id in possible_missions_ids:
            if await missions_service.get_by_id(id) is None:
                print(id)
                return False
        result = self.collection.update_one({"id": drone_id},
                                            {"$addToSet": {"possible_missions_ids": {"$each": possible_missions_ids}}})
        return result.modified_count > 0

    async def is_drone_id_valid(self, id: str):
        drone_entity = await self.get_by_id(id)
        if drone_entity is None:
            return True
        return False

    async def is_valid_drone_data(self, drone_data):
        results = await asyncio.gather(
            self.is_drone_id_valid(drone_data['id']),
            self.is_status_valid(drone_data['status'])
            # self.is_valid_missions_input(drone_data['current_mission_id']
            #                              , drone_data['possible_missions_ids']),
        )
        print(results)
        return all(results)

    # async def is_mission_in_possible_missions(self, current_mission: str, possible_missions_ids: set) -> bool:
    #     return current_mission in possible_missions_ids
    #
    # async def is_valid_missions_input(self, current_mission: str, possible_missions_ids: set) -> bool:
    #     if not await self.is_mission_in_possible_missions(current_mission, possible_missions_ids):
    #         return False
    #     mission_service = MissionsService(collection_missions)
    #     if possible_missions_ids:
    #         for mid in possible_missions_ids:
    #             mission = await mission_service.get_by_mission_id(mid)
    #             if mission is None:
    #                 return False
    #         return True
    #     else:
    #         return False

    async def update_current_mission(self, drone_id: str, current_mission: str = None):
        return self.collection.update_one({"id": drone_id},
                                          {"$set": {"current_mission_id": current_mission}})

    async def update(self, item_id: str, data: dict) -> Optional[dict]:
        pass

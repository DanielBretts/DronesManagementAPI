import asyncio
from typing import Optional
from pymongo.collection import Collection
from bson import ObjectId
from datetime import datetime, timedelta

from bl.service import Service
from config.database import collection_drones, collection_missions
from bl.missions_service import MissionsService
from bl.drones_service import DronesService
from dal.entities.schedule import Schedule
from utils.Constants import ScheduleStatus
from bl.trajectories_service import TrajectoriesService
from config.database import collection_trajectories


class ScheduleService(Service):

    async def get_all(self) -> list:
        return list(self.collection.find({}, {'_id': 0}))

    async def create(self, schedule_data: dict) -> dict:
        schedule_data['status'] = ScheduleStatus.SCHEDULED
        missions_service = MissionsService(collection_missions)
        mission = await missions_service.get_by_id(schedule_data['mission_id'])
        if not mission:
            return dict()
        schedule_data['end_time'] = self.set_end_time(schedule_data['start_time'], mission['duration'])
        if await self.is_valid_schedule_data(schedule_data, missions_service) is False:
            return dict()

        result = self.collection.insert_one(schedule_data)
        inserted_id = result.inserted_id
        inserted_schedule = self.collection.find_one({"_id": ObjectId(inserted_id)}, {'_id': 0})
        return inserted_schedule

    async def update(self, schedule_id: str, status: str) -> bool:
        if await self.is_status_valid(status):
            result = self.collection.update_one({"id": schedule_id}, {"$set": {"status": status}})
            return result.modified_count > 0
        else:
            return False

    async def get_schedules_date_range(self, start_date: datetime, end_date: datetime) -> list:
        return list(self.collection.find({"start_time": {"$gte": start_date}, "end_time": {"$lte": end_date}},
                                         {'_id': 0}))

    async def get_schedules_by_drone(self, drone_id: str) -> list:
        return list(self.collection.find({"drone_id": drone_id}, {'_id': 0}))

    async def is_valid_schedule_data(self, schedule_data: dict, missions_service: MissionsService):
        results = await asyncio.gather(
            self.is_drone_input_valid(schedule_data),
            self.is_schedule_id_valid(schedule_data['id']),
            self.is_mission_input_valid(schedule_data, missions_service),
            self.is_status_valid(schedule_data['status']),
            self.is_valid_time_range(schedule_data['start_time'], schedule_data['end_time']),
            self.get_overlapping_schedules_same_mission(schedule_data['start_time'],
                                                        schedule_data['mission_id']),
            self.is_drone_available(schedule_data)
        )

        results = list(results)
        print(results)
        return all(results)

    async def get_overlapping_schedules_same_mission(self, start_time: datetime,
                                                     mission_id: str) -> bool:
        missions_service = MissionsService(collection_missions)
        trajectory_service = TrajectoriesService(collection_trajectories)

        # Get the trajectory description for the provided mission
        mission = await missions_service.get_by_id(mission_id)
        trajectory = await trajectory_service.get_by_id(mission['trajectory_id'])
        print(trajectory)
        trajectory_description = trajectory['description']
        # Find overlapping schedules
        overlapping_schedules = list(self.collection.find({
            "start_time": {"$eq": start_time}
        }, {'_id': 0}))

        # Check if any overlapping schedule has the same trajectory description
        for schedule in overlapping_schedules:
            # Get the mission details for the schedule
            schedule_mission = await missions_service.get_by_id(schedule['mission_id'])
            # Get the trajectory details for the schedule
            schedule_trajectory = await trajectory_service.get_by_id(schedule_mission['trajectory_id'])
            print(schedule_trajectory)
            if schedule_trajectory['description'] == trajectory_description:
                return False

        return True

    async def is_mission_input_valid(self, schedule_data: dict, missions_service: MissionsService) -> bool:
        mission = await missions_service.get_by_id(schedule_data['mission_id'])
        if mission:
            return True
        else:
            return False

    async def is_drone_input_valid(self, schedule_data: dict) -> bool:
        drone_service = DronesService(collection_drones)
        drone = await drone_service.get_by_id(schedule_data['drone_id'])
        if drone:
            if schedule_data['mission_id'] in drone['possible_missions_ids']:
                return True
        return False

    async def is_status_valid(self, status: str) -> bool:
        return status in ScheduleStatus.__dict__.values()

    async def is_valid_time_range(self, start_time: datetime, end_time: datetime) -> bool:
        # Check if the time range is valid
        print(f"{start_time}  {end_time}")
        return start_time < end_time

    async def is_schedule_id_valid(self, id):
        schedule_entity = await self.get_by_id(id)
        if schedule_entity is None:
            return True
        return False

    async def get_by_id(self, schedule_id: str) -> Optional[dict]:
        return self.collection.find_one({"id": schedule_id}, {'_id': 0})

    # Retrieve schedules that involve the drone and overlap with the given time range
    async def get_overlapping_schedules(self, drone_id: str, start_time: datetime, end_time: datetime) -> list:
        overlapping_schedules = []
        for schedule in self.collection.find({
            "drone_id": drone_id,
            "start_time": {"$lt": end_time},
            "end_time": {"$gt": start_time}
        }, {'_id': 0})[:]:
            overlapping_schedules.append(schedule)

        return overlapping_schedules

    async def is_drone_available(self, schedule_data) -> bool:
        overlapping_schedules = await self.get_overlapping_schedules(schedule_data['drone_id'],
                                                                     schedule_data['start_time'],
                                                                     schedule_data['end_time'])
        print(overlapping_schedules)
        return not bool(overlapping_schedules)

    def set_end_time(self, schedule_data: datetime, duration: int) -> datetime:
        return schedule_data + timedelta(minutes=duration)

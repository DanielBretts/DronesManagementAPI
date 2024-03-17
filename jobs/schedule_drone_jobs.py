from datetime import datetime
from typing import List

from fastapi import APIRouter
from fastapi_utilities import repeat_every

from bl.drones_service import DronesService
from bl.schedule_service import ScheduleService
from config.database import collection_schedules, collection_drones
from utils.Constants import ScheduleStatus, DroneStatus
from utils.logger_config import log

router = APIRouter()

schedules_service = ScheduleService(collection_schedules)
drones_service = DronesService(collection_drones)


# Function to mark a drone as on mission
async def mark_drone_on_mission(drone_id: str, mission_id: str) -> None:
    await drones_service.update_drone_status(drone_id, DroneStatus.ON_MISSION)
    await drones_service.update_current_mission(drone_id, mission_id)


# Function to retrieve scheduled missions that are due to start
async def get_upcoming_missions(current_time: datetime) -> List[dict]:
    lst = list(collection_schedules.find({
        "status": {"$ne": ScheduleStatus.COMPLETED},
        "end_time": {"$gt": current_time}
    }))
    # print(lst)
    # for schedule in lst:
    #     send_notification(schedule['drone_id'], schedule['mission_id'], schedule['id'], schedule['start_time'])
    return lst


@router.on_event('startup')
@repeat_every(seconds=30)
async def check_due_missions():
    current_time = datetime.utcnow()

    log.info("Time is: " + str(current_time))
    upcoming_missions = await get_upcoming_missions(current_time)
    for active in upcoming_missions:
        mission_start_time = active["start_time"]
        mission_end_time = active["end_time"]
        # Check if the current time is past the start time
        if mission_start_time <= current_time <= mission_end_time:
            await handle_launched_mission(active)
        # Check if mission completed
        elif current_time > mission_end_time:
            await handle_finished_task(active)
        # This is to handle past schedules to set them to the correct status
        elif current_time < mission_start_time:
            await handle_past_mission(active)


async def handle_past_mission(active):
    await schedules_service.update(active['id'], ScheduleStatus.SCHEDULED)
    # Mark drone as available
    await drones_service.update_drone_status(active['drone_id'], DroneStatus.AVAILABLE)
    await drones_service.update_current_mission(active['drone_id'], None)


async def handle_launched_mission(active):
    active_drone = await drones_service.get_by_id(active['drone_id'])
    await schedules_service.update(active['id'], ScheduleStatus.IN_PROGRESS)
    if active_drone['status'] != DroneStatus.ON_MISSION:
        send_notification(active['drone_id'], active['mission_id'], active['id'], "Mission started")
        # Mark drone as on mission
        await mark_drone_on_mission(active['drone_id'], active['mission_id'])


async def handle_finished_task(active):
    send_notification(active['drone_id'], active['mission_id'], active['id'], "Mission completed")
    await schedules_service.update(active['id'], ScheduleStatus.COMPLETED)
    # Mark drone as available
    await drones_service.update_drone_status(active['drone_id'], DroneStatus.AVAILABLE)
    await drones_service.update_current_mission(active['drone_id'], None)


# “Alert” when a scheduled drone is going on its mission.
def send_notification(drone_id: str, mission_id: str, schedule_id: str, message: str):
    log.info(f"Notification for Drone {drone_id}: schedule {schedule_id} mission: {mission_id} {message}")

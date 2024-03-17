from datetime import datetime
from fastapi import APIRouter, HTTPException
from config.database import collection_schedules
from bl.schedule_service import ScheduleService
from dal.entities.schedule import Schedule

router = APIRouter(prefix="/schedule")
schedule_service = ScheduleService(collection_schedules)


# Endpoint to get all schedules
@router.get("/")
async def get_schedules():
    return await schedule_service.get_all()


# Endpoint to create a new schedule
@router.post("/")
async def create_schedule(schedule: Schedule):
    schedule_data = dict(schedule)
    result = await schedule_service.create(schedule_data)
    if result:
        return result
    else:
        raise HTTPException(status_code=400, detail="Failed to create schedule")


# Endpoint to update a schedule's status
@router.put("/{id}")
async def update_schedule_status(id: str, status: str):
    result = await schedule_service.update(id, status)
    if result:
        return {"message": "Schedule status updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Schedule/Status not found")


# Endpoint to get schedules within a date range
@router.get("/date_range/")
async def get_schedules_date_range(start_date: datetime, end_date: datetime):
    schedules = await schedule_service.get_schedules_date_range(start_date, end_date)
    if not schedules:
        raise HTTPException(status_code=404, detail="No schedules found within the specified date range")
    return schedules


# Endpoint to get schedules by drone
@router.get("/drone/{drone_id}")
async def get_schedules_by_drone(drone_id: str):
    schedules = await schedule_service.get_schedules_by_drone(drone_id)
    if not schedules:
        raise HTTPException(status_code=404, detail=f"No schedules found for drone with ID {drone_id}")
    return schedules

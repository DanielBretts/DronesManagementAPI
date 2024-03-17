from typing import List

from fastapi import APIRouter, HTTPException

from bl.missions_service import MissionsService
from config.database import collection_missions
from dal.entities.mission import Mission

router = APIRouter(prefix="/missions")
missions_service = MissionsService(collection_missions)


# Endpoint to get all missions
@router.get("/")
async def get_missions():
    missions = await missions_service.get_all()
    if not missions:
        raise HTTPException(status_code=404, detail="No missions found")
    return missions


# Endpoint to create a new mission
@router.post("/")
async def create_mission(mission: Mission):
    created_mission = await missions_service.create(dict(mission))
    if not created_mission:
        raise HTTPException(status_code=400, detail="Failed to create mission")
    return created_mission

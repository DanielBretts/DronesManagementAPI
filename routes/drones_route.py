from typing import List

from fastapi import APIRouter, HTTPException
from dal.entities.drone import Drone
from config.database import collection_drones
from bl.drones_service import DronesService

router = APIRouter(prefix='/drones')
drone_service = DronesService(collection_drones)

@router.get("/")
async def get_drones():
    drones = await drone_service.get_all()
    if not drones:
        raise HTTPException(status_code=404, detail="No missions found")
    return drones

# Endpoint to get all drones by availability status
@router.get("/findByStatus/{status}")
async def get_drones_by_status(status):
    drones = await drone_service.get_drones_by_status(status)
    if not drones:
        raise HTTPException(status_code=404, detail=f"No drones found with status {status}")
    return drones

# Endpoint to get a specific drone by ID
@router.get("/findById/{drone_id}")
async def get_drone_by_id(drone_id):
    drone = await drone_service.get_by_id(drone_id)
    if not drone:
        raise HTTPException(status_code=404, detail=f"No drone found with ID {drone_id}")
    return drone

# Endpoint to update a drone's status
@router.put("/{drone_id}")
async def update_drone_status(drone_id, status):
    updated_drone = await drone_service.update_drone_status(drone_id, status)
    if not updated_drone:
        raise HTTPException(status_code=404, detail=f"No drone found with ID {drone_id}")
    return updated_drone

# Endpoint to create a new drone
@router.post("/")
async def create_drone(drone: Drone):
    created_drone = await drone_service.create(dict(drone))
    if not created_drone:
        raise HTTPException(status_code=400, detail="Failed to create drone")
    return created_drone

# Endpoint to modify possible missions for a drone
@router.put("/{drone_id}/possible_missions")
async def modify_possible_missions(drone_id : str, possible_missions_ids: List[str]):
    success = await drone_service.modify_possible_missions(drone_id, possible_missions_ids)
    if not success:
        raise HTTPException(status_code=404, detail="One or more missions are invalid")
    return {"message": "Possible missions modified successfully"}
from typing import List

from fastapi import APIRouter, HTTPException

from bl.trajectories_service import TrajectoriesService
from config.database import collection_trajectories
from dal.entities.mission import Mission
from dal.entities.trajectory import Trajectory

router = APIRouter(prefix='/trajectories')
trajectories_service = TrajectoriesService(collection_trajectories)


# Endpoint to get all trajectories
@router.get("/")
async def get_trajectories():
    trajectories = await trajectories_service.get_all()
    if not trajectories:
        raise HTTPException(status_code=404, detail="No trajectories found")
    return trajectories


# Endpoint to create a new trajectory
@router.post("/")
async def create_trajectory(trajectory: Trajectory):
    created_trajectory = await trajectories_service.create(dict(trajectory))
    if created_trajectory:
        return created_trajectory
    else:
        raise HTTPException(status_code=400, detail="Failed to create trajectory")



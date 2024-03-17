from typing import Optional
from pydantic import BaseModel
from utils.Constants import DroneStatus

class Drone(BaseModel):
    id: str
    name: str
    status: Optional[str] = DroneStatus.AVAILABLE
    current_mission_id: Optional[str] = None
    possible_missions_ids: set[str] = set()

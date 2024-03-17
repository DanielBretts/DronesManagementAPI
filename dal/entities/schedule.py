from pydantic import BaseModel
from datetime import datetime

class Schedule(BaseModel):
    id: str
    drone_id: str
    mission_id: str
    start_time: datetime
    end_time: datetime = None
    status: str = None

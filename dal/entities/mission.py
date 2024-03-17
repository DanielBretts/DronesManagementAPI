
from pydantic import BaseModel


class Mission(BaseModel):
    id: str
    trajectory_id: str
    duration: int
    priority: int

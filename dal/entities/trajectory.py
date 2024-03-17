
from pydantic import BaseModel


class Trajectory(BaseModel):
    id: str
    description: str
    type: str
    number_of_products: int
    distance: int

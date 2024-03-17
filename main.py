from fastapi import FastAPI
from jobs.schedule_drone_jobs import router as drone_job
from routes.drones_route import router as drone_router
from routes.missions_route import router as mission_router
from routes.trajectories_route import router as trajectory_router
from routes.schedule_route import router as schedule_router

app = FastAPI()

app.include_router(drone_router)
app.include_router(mission_router)
app.include_router(trajectory_router)
app.include_router(schedule_router)
app.include_router(drone_job)



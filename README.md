
# Drone Mission Control API

This document provides the API documentation for the Drone Mission Control System. The system is designed to manage drones, missions, schedules, and trajectories.
Please ensure that you entered username and password in ```.env``` file to integrate with the database

##### Framework : FastAPI
##### Database : MongoDB

# Setup Instructions

- Install dependencies:

```bash
pip install -r requirements.txt
```
- Start the application:

```bash
uvicorn main:app --reload
```

# Technologies

- Amazon EC2: Launched an EC2 instance using ```13.60.42.212``` to host the application.
Docker and 
- Docker Compose: Containerized the application and its dependencies, managing them with Docker Compose.
- Watchtower: Integrated to automatically fetch updated container images from Docker Hub, ensuring the application stays current.

## Endpoints Overview

### Drones

- **GET /drones**: Retrieve all drones.
- **POST /drone**: Create a new drone.

**Request**:
```json
{
  "id": "drone123",
  "name": "DroonyX",
  "possible_missions_ids": ["1","2","3"]
}
```

**Response**:
```json
{
  "id": "drone123",
  "name": "DroonyX",
  "status": "available",
  "current_mission_id": null,
  "possible_missions_ids": [
    "2",
    "1",
    "3"
  ]
}
```

- **GET /drones/findByStatus/{status}**: Find all drones with specific status.

**Response**:
```json
[
  {
    "id": "1",
    "name": "Drono",
    "status": "available",
    "current_mission_id": null,
    "possible_missions_ids": [
      "123123"
    ]
  },
  {
    "id": "2",
    "name": "X23e",
    "status": "available",
    "current_mission_id": null,
    "possible_missions_ids": [
      "111111"
    ]
  },
  {
    "id": "drone123",
    "name": "DroonyX",
    "status": "available",
    "current_mission_id": null,
    "possible_missions_ids": [
        "2",
        "1",
        "3"
    ]
}
]
```

- **GET /drones/findById/{drone_id}**: Finds drone with the specific id.

**Response**:
```json
{
  "id": "drone123",
  "name": "DroonyX",
  "status": "available",
  "current_mission_id": null,
  "possible_missions_ids": [
    "2",
    "1",
    "3"
  ]
}
```

- **PUT /drones/{id}?status={status}**: Update the status of a specific drone.

**Response**:
```json
{
  "id": "drone123",
  "name": "DroonyX",
  "status": "on-mission",
  "current_mission_id": null,
  "possible_missions_ids": [
    "2",
    "1",
    "3"
  ]
}
```

- **PUT /drones/{id}/possible_missions**: Update the possible missions of a specific drone.

**Request Body**
```json
[
  "111111",
  "2",
  "3"
]
```

**Response**:
```json
{
  "message": "Possible missions modified successfully"
}
```

### Missions

- **GET /missions**: Retrieve all missions.

- **POST /missions**: Create a new mission.

**Request**:
```json
{
  "id": "1",
  "trajectory_id": "1",
  "duration": 25,
  "priority": 4
}
```

**Response**:
```json
{
  "id": "1",
  "trajectory_id": "1",
  "duration": 25,
  "priority": 4
}
```

### Schedule

- **GET /schedule**: Retrieve all schedules.
- **POST /schedule**: Create a new schedule.

**Request**:
```json
{
  "id": "1222",
  "drone_id": "drone123",
  "mission_id": "1",
  "start_time": "2024-03-10T11:51:08.858Z"
}
```

**Response**:
```json
{
  "id": "1222",
  "drone_id": "drone123",
  "mission_id": "1",
  "start_time": "2024-03-10T11:51:08.858000",
  "end_time": "2024-03-10T12:16:08.858000",
  "status": "scheduled"
}
```
- **PUT /schedule/{id}?status={status}**: Update the schedule status.

**Response**:
```json
{
  "message": "Schedule status updated successfully"
}
```

- **GET /schedule/date_range/?start_date={start_time}&end_date={end_time}**: Get all schedules in a date range.

**Response**:
```json
[
  {
    "id": "1222",
    "drone_id": "drone123",
    "mission_id": "1",
    "start_time": "2024-03-10T11:51:08.858000",
    "end_time": "2024-03-10T12:16:08.858000",
    "status": "completed"
  }
]
```

- **GET /schedule/drone/{drone_id}**: Get all schedules that a specific drone is assigned to.

**Response**:
```json
[
  {
    "id": "1222",
    "drone_id": "drone123",
    "mission_id": "1",
    "start_time": "2024-03-10T11:51:08.858000",
    "end_time": "2024-03-10T12:16:08.858000",
    "status": "completed"
  }
]
```

### Trajectories

- **GET /trajectories**: Retrieve all trajectories.

**Response**:
```json
[
  {
    "id": "1",
    "description": "Right Main Aisle",
    "type": "Straight line",
    "number_of_products": 10,
    "distance": 10
  },
  {
    "id": "2",
    "description": "Right Main Aisle",
    "type": "Zig-zag",
    "number_of_products": 25,
    "distance": 80
  }
]
```

- **POST /trajectories**: Create a new trajectory.

**Request**:
```json
{
  "id": "222",
  "description": "string",
  "type": "string",
  "number_of_products": 10,
  "distance": 10
}
```
**Response**:
```json
{
  "id": "3",
  "description": "string",
  "type": "string",
  "number_of_products": 10,
  "distance": 10
}
```

## Alert Implementation

When mission is launched - a relevant log message will appear in the console.

```bash
INFO - Notification for Drone 1: schedule id2 mission: 123123 Mission started
```
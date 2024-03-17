def drone_serial(drone) -> dict:
    return {
        'id': drone['id'],
        'name': drone['name'],
        'status': drone['status'],
        'current_mission_id': drone['current_mission_id'],
        'possible_missions_ids': drone['possible_missions_ids']
    }


def drone_list_serial(drones) -> list:
    return [drone_serial(drone) for drone in drones]


def mission_serial(mission) -> dict:
    return {
        'id': mission['id'],
        'trajectory_id': mission['trajectory_id'],
        'duration': mission['duration'],
        'priority': mission['priority'],
    }


def mission_list_serial(missions) -> list:
    return [mission_serial(mission) for mission in missions]


def trajectory_serial(trajectory) -> dict:
    return {
        'id': trajectory['id'],
        'description': trajectory['description'],
        'type': trajectory['type'],
        'number_of_products': trajectory['number_of_products'],
        'distance': trajectory['distance']
    }


def trajectory_list_serial(trajectories) -> list:
    return [trajectory_serial(trajectory) for trajectory in trajectories]


def schedule_serial(schedule) -> dict:
    return {
        'id': schedule['id'],
        'drone_id': schedule['drone_id'],
        'mission_id': schedule['mission_id'],
        'start_time': schedule['start_time'],
        'end_time': schedule['end_time'],
        'status': schedule['status']
    }


def schedules_list_serial(schedules) -> list:
    return [schedule_serial(schedule) for schedule in schedules]

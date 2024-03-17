import asyncio
import collections
import csv
from datetime import datetime, timezone
from config import database as db
import ast
from config.database import collection_missions, collection_schedules, collection_trajectories, collection_drones


async def csv_to_mongodb(csv_file, collection_name):
    with open(csv_file, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile)
        header = reader.fieldnames

        for each in reader:
            row = {}
            for field in header:
                if field == 'start_time' or field == 'end_time':
                    date_obj = datetime.strptime(each[field], '%Y-%m-%d %H:%M:%S %Z')
                    row[field] = date_obj
                elif field == 'possible_missions_ids':
                    row[field] = [str(id) for id in ast.literal_eval(each[field])]
                elif field in ['duration', 'priority', 'number_of_products', 'distance']:
                    row[field] = int(each[field])
                else:
                    row[field] = each[field]
            collection_name.insert_one(row)


files_to_collections = {
    '../files/DronesDB.csv': collection_drones,
    '../files/MissionsDB.csv': collection_missions,
    '../files/TrajectoriesDB.csv': collection_trajectories,
    '../files/SchedulesDB.csv': collection_schedules}


async def write_all_to_mongo():
    for file_path, collection in files_to_collections.items():
        await csv_to_mongodb(file_path, collection)


if __name__ == '__main__':
    asyncio.run(write_all_to_mongo())

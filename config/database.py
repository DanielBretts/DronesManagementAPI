import os
import ssl

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_pass = os.getenv("MONGO_PASS")
mongo_user = os.getenv("MONGO_USER")

uri = f"mongodb+srv://{mongo_user}:{mongo_pass}@homeassignment.miynwen.mongodb.net/?retryWrites=true&w=majority"

client = MongoClient(uri,ssl_cert_reqs=ssl.CERT_NONE)

db = client.WDS_db

collection_drones = db["drones"]

collection_missions = db["missions"]

collection_trajectories = db["trajectories"]

collection_schedules = db["schedules"]
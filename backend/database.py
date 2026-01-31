from pymongo import MongoClient

MONGO_URL = "mongodb+srv://hrmsuser:Viraj%402003@hrms.eff28sy.mongodb.net/?appName=hrms"

client = MongoClient(MONGO_URL)

db = client["hrms_lite"]

def get_database():
    return db
